from __future__ import print_function # allows us to easily print to the same line twice
from sets import Set
from Reaction import Reaction
from Errors import FileFormatError

class CRN:
	def __init__(self, diff_eq_txt = None, crn_txt = None):
		self.Species = Set()
		self.Reactions = Set()

		if (diff_eq_txt):
			self.from_diff_eq(diff_eq_txt)

	# This should follow the specifications we discussed Monday
	# .txt created straight from GUI
	def from_diff_eq(self, file_name):
		f = open(file_name, 'r')
		
		# get number of species
		line = f.readline()
		
		if (line[-1] != '\n'):
			f.close()
			raise FileFormatError('Number of species missing.')
		
		num_species = int(line.split()[0])
		
		# get species
		line = f.readline()
		
		if (line[-1] != '\n'):
			f.close()
			raise FileFormatError('Species names missing.')
		
		self.Species.update( line.split() )
		
		if (num_species != len(self.Species)):
			f.close()
			raise FileFormatError('Invalid number of species names.')
		
		# get species and num_terms
		for i in range(num_species):
			line = f.readline()
			
			if (line[-1] != '\n'):
				f.close()
				raise FileFormatError('Species header missing.')
			
			list = line.split()
			spec = list[0]
			num_terms = int(list[1])
			
			#get terms
			for j in range(num_terms):
				line = f.readline()
				
				if (j != num_terms - 1 and line[-1] != '\n'):
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
					
					if (exp_list[0] not in self.Species):
						f.close()
						raise FileFormatError('Invalid species.')
						
					reactant_dict[exp_list[0]] = int(exp_list[1])
				
				# products
				product_dict = {}
				
				for reactant, coefficient in reactant_dict.iteritems():
					if (reactant != spec):
						product_dict[reactant] = coefficient
				
				coeff = reactant_dict.get(spec, 0)
				
				if (negative and coeff < 1):
					f.close()
					raise FileFormatError('Illegal differential equation.')
				elif (negative and coeff > 1):
					product_dict[spec] = coeff - 1
				elif (not negative):
					product_dict[spec] = coeff + 1

				
				reaction = Reaction(rate_coeff, rate_var, reactant_dict, product_dict)
				self.Reactions.add(reaction)

		
		line = f.readline()
		
		if (line):
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
				
				if (first):			# if we are printing our first species...
					plus_sign = '' 	# just print an empty string instead of a plus
					first = False

				line.append(plus_sign)
				
				if (coefficient != 1):
					line.append(str(coefficient))
					
				line.append(str(species))

			line.append( ' -> ' )
			first = True
			
			# products
			for species, coefficient in reaction.products.iteritems():
				plus_sign = ' + '
				
				if (first):
					plus_sign = ''
					first = False

				line.append(plus_sign)
				
				if (coefficient != 1):	# Don't print the coefficient if it is 1
					line.append(str(coefficient))
					
				line.append(str(species))
			
			# reaction rate
			line.append(' at rate ')
			
			if (reaction.rate_coeff != 1):
				line.append( str(reaction.rate_coeff) + '*')
			
			line.append( reaction.rate_var )
			
			# full reaction
			to_print.append(''.join(line))

		if (file_name):
			with open( file_name, 'w' ) as output:
				for line in to_print:
					output.write(line + '\n')

		if(console):
			for line in to_print:
				print(line)

	
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
				
				if (stoich == 0):
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
		
		if (file_name):
			with open( file_name, 'w' ) as output:
				for line in to_print:
					output.write(line + '\n')
		
		if (console):
			for line in to_print:
				print(line)
