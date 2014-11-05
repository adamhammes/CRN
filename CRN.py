from __future__ import print_function # allows us to easily print to the same line twice
from sets import Set
from Reaction import Reaction
from Errors import FileFormatError

class CRN:
	def __init__(self, diff_eq_txt = None, crn_txt = None):
		self.species = Set()
		self.reactions = Set()

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
			# if
		
		num_species = int(line.split()[0])
		
		# get species
		line = f.readline()
		
		if (line[-1] != '\n'):
			f.close()
			raise FileFormatError('Species names missing.')
			# if
		
		self.species.update(set(line.split()))
		
		if (num_species != len(self.species)):
			f.close()
			raise FileFormatError('Invalid number of species names.')
			# if
		
		# get species and num_terms
		for i in range(num_species):
			line = f.readline()
			
			if (line[-1] != '\n'):
				f.close()
				raise FileFormatError('Species header missing.')
				# if
			
			list = line.split()
			spec = list[0]
			num_terms = int(list[1])
			
			#get terms
			for j in range(num_terms):
				line = f.readline()
				
				if (j != num_terms - 1 and line[-1] != '\n'):
					f.close()
					raise FileFormatError('Term missing.')
					# if
				
				list = line.split()
				
				# sign
				negative = (list[0][0] == '-')
				
				# rate
				rate_list = list[0].split(':')
				rate_coeff = int(rate_list[0].strip('-')
				rate_var = rate_list[1]
				
				# reactants
				reactant_dict = {}
				
				for k in range(1, len(list)):
					exp_list = list[k].split(':')
					
					if (exp_list[0] not in self.species):
						f.close()
						raise FileFormatError('Invalid species.')
						# if
						
					reactant_dict[exp_list[0]] = int(exp_list[1])
					# for
				
				# products
				product_dict = {}
				
				for reactant, coefficient in reactant_dict.iteritems():
					if (reactant != spec):
						product_dict[reactant] = coefficient
						# if
					# for
				
				coeff = reactant_dict.get(spec, 0)
				
				if (negative and coeff < 1):
					f.close()
					raise FileFormatError('Illegal differential equation.')
				elif (negative and coeff > 1):
					product_dict[spec] = coeff - 1
				elif (not negative):
					product_dict[spec] = coeff + 1
					# if
				
				reaction = Reaction(rate_coeff, rate_var, reactant_dict, product_dict)
				self.reactions.add(reaction)
				# for
			# for
		
		line = f.readline()
		
		if (line):
			f.close()
			raise FileFormatError('File too long.')
			# if
		
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
					# if

				line.append(plus_sign)
				
				if (coefficient != 1):
					line.append(str(coefficient))
					# if
					
				line.append(str(species))
				# for

			line.append( ' -> ' )
			first = True
			
			# products
			for species, coefficient in reaction.products.iteritems():
				plus_sign = ' + '
				
				if (first):
					plus_sign = ''
					first = False
					# if

				line.append(plus_sign)
				
				if (coefficient != 1):	# Don't print the coefficient if it is 1
					line.append(str(coefficient))
					# if
					
				line.append(str(species))
				# for
			
			# reaction rate
			line.append(' (Reaction Rate = ')
			
			if (reaction.rate_coeff != 1):
				line.append(str(reaction.rate_coeff))
				# if
			
			line.append('[')
			line.append(str(reaction.rate_var))
			line.append('])')
			
			# full reaction
			to_print.append(''.join(line))
			# for

		if (file_name):
			output = open(file_name, 'w')
			
			for line in to_print:
				output.write(line + '\n')
				# for
				
			output.close()
			# if

		if(console):
			for line in to_print:
				print(line)
				# for
			# if
	
	# Prints the differential equations which describe the behavior of
	# this CRN to the console
	def diff_eq_print(self, file_name = None, console = None):
		to_print = []
		
		# first line = number of species
		line = []
		line.append(str(len(self.species)))
		to_print.append(''.join(line))
		
		# second line = list of species
		line = []
		first = True
		
		for spec in self.species:
			space = ' '
			
			if (first):
				space = ''
				first = False
				# if
			
			line.append(space)
			line.append(str(spec))
			# for
		
		to_print.append(''.join(line))
		
		# differential equations
		for spec in self.species:
			space = ' '
			species_block = []
			count = 0
			
			for reaction in self.reactions:
				stoich = reaction.stoichiometry(spec)
				
				if (stoich == 0):
					continue
					# if
				
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
					# for
				
				species_block.append(''.join(line))
				count += 1
				# for
			
			# first line = species_name num_terms
			line = []
			line.append(str(spec))
			line.append(space)
			line.append(str(count))
			to_print.append(''.join(line))
			
			# terms
			for line in species_block:
				to_print.append(''.join(line))
				# for
			# for
		
		if (file_name):
			output = open(file_name, 'w')
			
			for line in to_print:
				output.write(line + '\n')
				# for
			
			output.close()
			# if
		
		if (console):
			for line in to_print:
				print(line)
				# for
			# if
