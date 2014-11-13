from __future__ import print_function # allows us to easily print to the same line twice
from __future__ import unicode_literals
from Reaction import Reaction
from Errors import FileFormatError
import re
import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class CRN:
	def __init__(self, diff_eq_txt = None, crn_txt = None, eq_text = None):
		self.Species = set()
		self.Reactions = set()

		if diff_eq_txt:
			self.from_diff_eq(diff_eq_txt)

		if eq_text:
			self.from_equations( eq_text )


	def from_equations( self, file_name ):
		f = self.safe_open( file_name )
		if not f:
			return

		to_print = []
		lines = []
		for line in f:
			stripped = line.strip()
			if stripped:
				lines.append( stripped )

		f.close()

		# pull all the species from the left side of the equation
		for line in lines:
			var_re = re.compile( '([^\W\d_](_\d+)?)', re.UNICODE )
			spec = var_re.match( line ).group()
			self.Species.add( spec )

		to_print.append( str( len( self.Species ) ) )
		string = ''
		for species in self.Species:
			string += species
			string += ' '
		to_print.append( string.rstrip() )

		for line in lines:
			var, terms = line.split( '=' )
			terms.strip()

			var.strip()	
			
			var_re = re.compile( '([^\W\d_](_\d+)?)', re.UNICODE )
			spec = var_re.match( line ).group()

			terms = terms.replace( ' ', '' )
			terms = terms.replace ('+-', '-' )
			terms = terms.replace ('-+', '-' )
			terms = terms.replace( '+', ' +' )
			terms = terms.replace( '-', ' -' )

			terms = terms.split()
			if not terms[0].startswith( '-' ):
				terms[0] = '+' + terms[0]

			if spec not in self.Species:
				raise FileFormatError( "Invalid species name" )
				return
			else:
				to_print.append( spec + ' ' + str( len( terms ) ) )


			# Now terms hold each term with no whitespace
			# and with a +/- in front 

			
			for term in terms:
				to_add = []
				# optional plus or minus, any number of digits, single character 
				# variable name, optional underscore+ single character subscript
				rate_re = re.compile( r'''
						([+-]?\d*)
						([^\W\d_])
						(_\d+)?
					''', re.VERBOSE | re.UNICODE )

				match = rate_re.match( term )
				coeff = match.group(1)
				var = match.group(2)
				sub = match.group(3)

				if len( coeff ) <= 1:
					coeff = '1'
				elif coeff == '-':
					coeff = '-1'

				if coeff.startswith( '+' ):
					coeff = coeff[1:]

				if not sub:
					sub = ''

				to_add.append( '%s:%s%s' %(coeff, var, sub ) )
				exp_term = term[match.end():]


				exps_re = re.compile( r'''
					([^\W\d_])
					(?:(_\d+))?
					(?:\^(\d+))?
					''', re.VERBOSE | re.UNICODE )

				entries = re.findall( exps_re, exp_term )
				for entry in entries:
					exp = entry[2]
					if not exp:
						exp = '1'
					to_add += ' %s%s:%s' %(entry[0], entry[1], exp)

				to_print.append( ''.join( to_add ) )

		self.array_print( to_print, file_name = 'temp.txt' )
		self.from_diff_eq( 'temp.txt' )
		os.remove( 'temp.txt' )




	# This should follow the specifications we discussed Monday
	# .txt created straight from GUI
	def from_diff_eq(self, file_name):
		f = self.safe_open( file_name )
		if not f:
			return

		# get number of species
		line = f.readline()
		
		if line[-1] != '\n':
			f.close()
			raise FileFormatError('Number of species missing.')
		
		num_species = int(line.split()[0])
		
		# get species
		line = f.readline()
		
		if line[-1] != '\n':
			f.close()
			raise FileFormatError('Species names missing.')
		
		self.Species.update( line.split() )
		
		if num_species != len(self.Species):
			f.close()
			raise FileFormatError('Invalid number of species names.')
		
		# get species and num_terms
		for i in range(num_species):
			line = f.readline()
			
			if line[-1] != '\n':
				f.close()
				raise FileFormatError('Species header missing.')
			
			list = line.split()
			spec = list[0]
			num_terms = int(list[1])
			
			#get terms
			for j in range(num_terms):
				line = f.readline()
				
				if j != num_terms - 1 and line[-1] != '\n':
					f.close()
					raise FileFormatError('Term missing.')
				
				list = line.split()
				
				# sign
				negative = (list[0][0] == '-')
				
				# rate
				rate_list = list[0].split(':')
				rate_coeff = int( rate_list[0].strip('-') )
				rate_var = rate_list[1]
				
				# reactants
				reactant_dict = {}
				
				for k in range(1, len(list)):
					exp_list = list[k].split(':')
					
					if exp_list[0] not in self.Species:
						f.close()
						raise FileFormatError('Invalid species.')
						
					reactant_dict[exp_list[0]] = int(exp_list[1])
				
				# products
				product_dict = {}
				
				for reactant, coefficient in reactant_dict.iteritems():
					if reactant != spec:
						product_dict[reactant] = coefficient
				
				coeff = reactant_dict.get(spec, 0)
				
				if negative and coeff < 1:
					f.close()
					raise FileFormatError('Illegal differential equation.')
				elif negative and coeff > 1:
					product_dict[spec] = coeff - 1
				else:
					product_dict[spec] = coeff + 1

				
				reaction = Reaction(rate_coeff, rate_var, reactant_dict, product_dict)
				self.Reactions.add(reaction)

		
		line = f.readline()
		
		if line:
			f.close()
			raise FileFormatError('File too long.')
		
		f.close()

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
		to_print = []
		
		for reaction in self.Reactions:
			line = []
			first = True
			# 'first' keeps track of when to write a + (don't write plus before first item)
			# we don't want to print something like this : ' + A + B -> C'
			
			# reactants
			for species, coefficient in reaction.reactants.iteritems():
				plus_sign = ' + '
				
				if first:			# if we are printing our first species...
					plus_sign = '' 	# just print an empty string instead of a plus
					first = False

				line.append(plus_sign)
				
				if coefficient != 1:
					line.append(str(coefficient))
					
				line.append(str(species))

			line.append( ' -> ' )
			first = True
			
			# products
			for species, coefficient in reaction.products.iteritems():
				plus_sign = ' + '
				
				if first:
					plus_sign = ''
					first = False

				line.append(plus_sign)
				
				if coefficient != 1:	# Don't print the coefficient if it is 1
					line.append(str(coefficient))
					
				line.append(str(species))
			
			# reaction rate
			line.append(' at rate ')
			
			if reaction.rate_coeff != 1:
				line.append( str(reaction.rate_coeff) + reaction.rate_var )
			
			# full reaction
			to_print.append(''.join(line))

		self.array_print( to_print, file_name, console)

	
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
