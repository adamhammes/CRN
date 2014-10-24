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
	def console_print( self ):
		for reaction in reactions:
			first = True 
			# 'first' keeps track of when to write a + (don't write plus before first item)
			# we don't want to print something like this : ' + A + B -> C'
			for species, coefficient in reaction.reactants.iteritems():
				to_print = []
				plus_sign = ' + '
				if( first ):			# if we are printing our first species...
					plus_sign = '' 		# just print an empty string instead
					first = False

				to_print.add( plus_sign )
				to_print.add( str( coefficient ) )
				to_print.add( str( species ) )

				print( ''.join( to_print ), end = '' ) # 'end' specifies what to end the line with; default is '\n'

			print( ' -> ', end = '' )

			to_print = [] # clear the list for the products now
			first = True
			for species, coefficient in reaction.products.iteritems():
				to_print = []
				plus_sign = ' + '
				if( first ):
					plus_sign = ''
					first = False

				to_print.add( plus_sign )
				to_print.add( str( coefficient ) )
				to_print.add( str( species ) )

				print( ''.join( to_print ), end = '' )

			print( '' ) # done printing the reaction, print newline


