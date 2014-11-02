from __future__ import print_function # allows us to easily print to the same line twice
from sets import Set
from Reaction import Reaction


class CRN:
	def __init__(self, gui_txt, readable_txt):
		species = Set()
		reactions = Set()

		if( gui_txt ):
			self.from_gui( gui_txt )


	# This should follow the specifications we discussed Monday
	# .txt created straight from GUI
	def from_gui(self, file_name):
		f = open( file_name, 'r' )
		#TODO: read file, fill up species/reactions
		f.close()

	# Option to read from a more human-friendly format e.g.
	# A + B -> C, D -> E, etc.
	# Specification not well defined yet!
	def from_readable( self, file_name ):
		f = open( file_name, 'r' )
		#TODO: read file, fill up species/reactions
		f.close()

	# Print reactions in CRN to the console as such:
	# A + B -> C
	# D -> E
	# etc.
	def nice_print( self, filename, console ):
		to_print = []
		for reaction in reactions:
			line = []
			first = True 
			# 'first' keeps track of when to write a + (don't write plus before first item)
			# we don't want to print something like this : ' + A + B -> C'
			for species, coefficient in reaction.reactants.iteritems():
				plus_sign = ' + '
				if( first ):			# if we are printing our first species...
					plus_sign = '' 		# just print an empty string instead of a plus
					first = False

				line.append( plus_sign )
				line.append( str( coefficient ) )
				line.append( str( species ) )

			line.append( ' -> ' )

			first = True
			for species, coefficient in reaction.products.iteritems():
				plus_sign = ' + '
				if( first ):
					plus_sign = ''
					first = False

				line.append( plus_sign )
				line.append( str( coefficient ) )
				line.append( str( species ) )

			to_print.append( ''.join(line) )

		if( filename ):
			f.open( filename, 'w' )
			
			for line in to_print:
				f.write( line + '\n' )

			f.close()

		if( console ):
			for line in to_print:
				print( line )
	
	# Prints CRN to console in diff eq format
	def diff_eq_print(self, filename, console):
		to_print = []

		# first line = number of species
		line = []
		line.append(str(len(species)))
		to_print.append(''.join(line))

		# second line = list of species
		line = []

		for spec in species:
			line.append( str( species ) + ' ' )

		to_print.append(''.join(line))

		# diff eq descriptions
		for spec_lhs in species: #lhs indicates this is the species whose equation we are on
			space = ' '
	    		species_block = []
	    		count = 0

	    		for reac in reactions:
	        		stoich = reac.stoichiometry(spec_lhs)

	        		if stoich == 0:
	            			continue

					# coefficient
	        		line = []
	        		prefix = ''
	        		if stoich == 1:
	            			prefix = ''
	        		elif stoich == -1:
	            			prefix = '-'
	        		else:
	            			prefix = str(stoich)

					line.append(prefix)
					line.append(str(reac.rate))

					# exponents
					for spec_rhs in species: #rhs indicates this species appears in a term of the equation
						line.append(space)
						line.append(str(spec_rhs))
						line.append(':')
	        				line.append(str(reac.reactants.get(spec_rhs, 0)))
	            		
	            		species_block.append(''.join(line))
	            		count += 1
	            	
			# first line = species num_terms
			line = []
			line.append(str(s))
			line.append(space)
			line.append(str(count))
			
			to_print.append(''.join(line))
			
			#terms
			for line in species_block:
				to_print.append(''.join(line))

		if filename:
			f.open(filename, 'w')
		
			for line in to_print:
				f.write(line + '\n')

	    		f.close()

		if console:
			for line in to_print:
				print(line)

