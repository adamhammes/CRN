from __future__ import print_function # allows us to easily print to the same line twice
from sets import Set
from Reaction import Reaction


class CRN:
	def __init__(self, gui_txt, readable_txt):
		species = Set()
		reactions = Set()

		if( gui_txt ):
			self.from_gui( gui_txt )


	# This should follow the specifications we discuused Monday
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
	# TODO: option to print to file
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

				line.add( plus_sign )
				line.add( str( coefficient ) )
				line.add( str( species ) )

				print( ''.join( line ), end = '' ) # 'end' specifies what to end the line with; default is '\n'

			line.add( ' -> ' )

			first = True
			for species, coefficient in reaction.products.iteritems():
				plus_sign = ' + '
				if( first ):
					plus_sign = ''
					first = False

				line.add( plus_sign )
				line.add( str( coefficient ) )
				line.add( str( species ) )

			to_print.add( ''.join(line) )

		if( filename ):
			f.open( filename, 'w' )
			
			for line in to_print:
				f.write( line + '\n' )

			f.close()

		if( console ):
			for line in to_print:
				print( line )






