from __future__ import print_function # allows us to easily print to the same line twice
from __future__ import unicode_literals
from Errors import FileFormatError
import re
import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

4
class Reaction:
	def __init__(self, rate_coeff, rate_var, reactants, products):
		self.rate_coeff = rate_coeff
		self.rate_var = rate_var
		self.reactants = reactants
		self.products = products
	
	def stoichiometry(self, species):
		return self.products.get(species, 0) - self.reactants.get(species, 0)

class CRN:


	def __init__(self, diff_eq_txt = None, crn_txt = None, eq_text = None):
		self.Species = set()
		self.Reactions = set()

		if diff_eq_txt:
			self.from_diff_eq(diff_eq_txt)

		if eq_text:
			self.from_equations( eq_text )

	def __str__( self ):
		return self.crn_print


	def from_equations( self, array):
		to_print = []
		lines = []
		for line in array:
			stripped = line.strip()
			if stripped:
				lines.append( stripped )


		# pull all the species from the left side of the equation

		for line_num, line in enumerate(lines):
			if line.find('=') == -1:
				raise FileFormatError('Line %d is not an equation' %(line_num))

			var_re = re.compile( '([^\W\d_](_\d+)?)', re.UNICODE )
			match = var_re.match(line)

			if not match:
				raise FileFormatError( "Illegal species name - left side of line " + str( line_num + 1 ) )
				Species.clear()
				return

			spec = var_re.match( line ).group()
			self.Species.add( spec )

		to_print.append( str( len( self.Species ) ) )
		string = ''
		for species in self.Species:
			string += species
			string += ' '
		to_print.append( string.rstrip() )

		for line_num, line in enumerate(lines):
			var, terms = line.split( '=' )
			terms.strip()

			var.strip()	
			
			variable_re = re.compile( '([^\W\d_](_\d+)?)', re.UNICODE )
			match = variable_re.match( line )
			if not match:
				raise FileFormatError( "Illegal species name - left side of line " + str( line_num + 1 ) )
				return
			spec = match.group()

			terms = terms.replace( ' ', '' )
			terms = terms.replace ('+-', '-' )
			terms = terms.replace ('-+', '-' )
			terms = terms.replace( '+', ' +' )
			terms = terms.replace( '-', ' -' )

			terms = terms.split()
			if not terms[0].startswith( '-' ):
				terms[0] = '+' + terms[0]

			if spec not in self.Species:
				raise FileFormatError( "Species not in CRN- left side of line " + str( line_num )  )
				return
			else:
				to_print.append( spec + ' ' + str( len( terms ) ) )


			# Now terms hold each term with no whitespace
			# and with a +/- in front 

			term_num = 1
			for term_num, term in enumerate(terms):
				to_add = []
				# optional plus or minus, any number of digits, single character 
				# variable name, optional underscore+ single character subscript
				rate_re = re.compile( r'''
						([+-]?\d*)
						([^\W\d_])
						(_\d+)?
					''', re.VERBOSE | re.UNICODE )

				match = rate_re.match( term )

				if not match:
					raise FileFormatError( 'Illegal term, line %d term %d ' %(line_num, term_num) )
					return

				coeff = match.group(1)
				variable = match.group(2)
				sub = match.group(3)

				if not sub:
					sub = ''

				rate_constant = str(variable + sub)

				if len( coeff ) <= 1:
					coeff = '1'
				elif coeff == '-':
					coeff = '-1'

				if coeff.startswith( '+' ):
					coeff = coeff[1:]


				to_add.append( '%s:%s%s' %(coeff, variable, sub ) )
				exp_term = term[match.end():]


				exps_re = re.compile( r'''
					([^\W\d_])
					(?:(_\d+))?
					(?:\^(\d+))?
					''', re.VERBOSE | re.UNICODE )

				entries = re.findall( exps_re, exp_term )
				for entry in entries:
					if not entry:
						raise FileFormatError( 'Invalid term - line %d term %d' (line_num, term_num))

					spec = entry[0] + entry[1]
					if spec not in self.Species:
						raise FileFormatError( 'Species \'%s\' not in CRN- line %d term %d' %(spec, line_num, term_num ))

					exp = entry[2]
					if not exp:
						exp = '1'
					to_add += ' %s%s:%s' %(entry[0], entry[1], exp)

				to_print.append( ''.join( to_add ) )
				term_num += 1
			line_num += 1

		self.from_diff_eq( to_print )


	# This should follow the specifications we discussed Monday
	# .txt created straight from GUI
	def from_diff_eq(self, string):
		index = 0
		max_index = len(string) - 1
		
		# get number of species
		if max_index == -1:
			raise FileFormatError('Species count missing.')
		
		line = string[index]
		index += 1
		num_species = int(line.split()[0])
		
		# get species
		if max_index == 1 and num_species != 0:
			raise FileFormatError('Species names missing.')
		
		if max_index > 1 and num_species == 0:
			raise FileFormatError('String too long.')
			
		line = string[index]
		index += 1
		self.Species.update( line.split() )
		
		if num_species != len(self.Species):
			raise FileFormatError('Invalid number of species names.')
		
		# get species and num_terms
		for i in range(num_species):
			if index > max_index:
				raise FileFormatError('Species header missing.')
			
			line = string[index]
			index += 1
			header = line.split()
			spec = header[0]
			num_terms = int(header[1])
			
			#get terms
			for j in range(num_terms):
				if index > max_index:
					raise FileFormatError('Term missing.')
					
				line = string[index]
				index += 1
				term = line.split()
				
				# sign
				negative = (term[0][0] == '-')
				
				# rate
				rate = term[0].split(':')
				rate_coeff = int(rate[0].strip('-'))
				rate_var = rate[1]
				
				# reactants
				reactant_dict = {}
				
				for k in range(1, len( term )):
					exp_list = term[k].split(':')
					
					if exp_list[0] not in self.Species:
						raise FileFormatError('Invalid species.')
						
					reactant_dict[exp_list[0]] = int(exp_list[1])
				
				# products
				product_dict = {}

				for reactant, coefficient in reactant_dict.iteritems():
					if reactant != spec:
						product_dict[reactant] = coefficient
				
				coeff = reactant_dict.get(spec, 0)
				
				if negative and coeff < 1:
					raise FileFormatError('Illegal differential equation.')
				elif negative and coeff > 1:
					product_dict[spec] = coeff - 1
				else:
					product_dict[spec] = coeff + 1

				reaction = Reaction(rate_coeff, rate_var, reactant_dict, product_dict)
				self.Reactions.add(reaction)

		
		if index < max_index:
			raise FileFormatError('String too long.')

	# Option to read from a more human-friendly format e.g.
	# A + B -> C, D -> E, etc.
	# Specification not well defined yet!
	def from_crn(self, file_name):
		f = open(file_name, 'r')
		#TODO: read file, fill up species/reactions
		f.close()

	# Print reactions in CRN to the console as such:
	# A + B -> C
	# D -> E
	# etc.
	def crn_print(self, file_name = None, console = None):
		print( 'crn_print')
		to_print = []
		
		for reaction in self.Reactions:
			line = []
			first = True
			# 'first' keeps track of when to write a + (don't write plus before first item)
			# we don't want to print something like this : ' + A + B -> C'
			
			# reactants
			side = []
			for species, coefficient in reaction.reactants.iteritems():
				side.append(species)
				if coefficient != 1:
					side[-1] = str(coefficient) + side[-1]	

			line.append( ' + '.join(side))
			line.append( ' -> ' )
			first = True
			
			# products
			side = []
			for species, coefficient in reaction.products.iteritems():
				side.append(species)
				if coefficient != 1:
					side[-1] = str(coefficient) + side[-1]	

			line.append( ' + '.join(side))
			
			# reaction rate
			line.append(' at rate ')
			
			if reaction.rate_coeff != 1:
				line.append( str(reaction.rate_coeff) )
			line.append( reaction.rate_var )
			
			# full reaction
			to_print.append(''.join(line))

		self.array_print( to_print, file_name, console)

		return '\n'.join( to_print )

	
	# Prints the differential equations which describe the behavior of
	# this CRN to the console
	def diff_eq_print(self, file_name = None, console = None):
		to_print = []
		
		# first line = number of species
		to_print.append( str( len( self.Species ) ) )
		
		# second line = list of species
		line = []
		first = True
		
		for spec in self.Species:			
			line.append( spec + ' ' )
		
		to_print.append( ''.join(line).rstrip() )
		
		# differential equations
		for spec in self.Species:
			space = ' '
			species_block = []
			count = 0
			
			for reaction in self.Reactions:
				stoich = reaction.stoichiometry(spec)
				
				if stoich == 0:
					continue
				
				# coefficient
				line = []				
				coeff = reaction.rate_coeff * stoich
				line.append(str(coeff))
				line.append(':')
				line.append(str(reaction.rate_var))
				
				# exponents
				for reactant, coefficient in reaction.reactants.iteritems():
					line.append(space)
					line.append(str(reactant))
					line.append(':')
					line.append(str(coefficient))
				
				species_block.append(''.join(line))
				count += 1
			
			# first line = species_name num_terms
			to_print.append( spec + ' ' + str(count) )
			
			# terms
			for line in species_block:
				to_print.append(''.join(line))

			self.array_print( to_print, file_name, console)
		

	def safe_open( self, file_name ):
		try:
			f = open(file_name, 'r')
		except IOError as e:
			print( e )
			return None
		return f

	def array_print( self, to_print, file_name = None, console = None ):
		if file_name:
			try:
				with open( file_name, 'w' ) as output:
					for line in to_print:
						output.write(line + '\n')
			except IOError as e:
				print('IOError: ' + e)
		
		if console:
			for line in to_print:
				print(line)
