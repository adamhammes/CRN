from __future__ import print_function
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
		f = open( file_name, "r" )
		#TODO: read file, fill up species/reactions
		f.close()

	# Option to read from a more human-friendly format e.g.
	# A + B -> C, D -> E, etc.
	# Specification not well defined yet!
	def from_readable( self, file_name ):
		f = open( file_name, "r" )
		#TODO: read file, fill up species/reactions
		f.close()

	def console_print( self ):
		for reaction in reactions:
			first = True
			for species, coefficient in reaction.reactants.iteritems():
				to_print = []
				plus_sign = " + "
				if( first ):
					plus_sign = ""
					first = False

				to_print.add( plus_sign )
				to_print.add( str( coefficient ) )
				to_print.add( str( species ) )

				print( ''.join( to_print ), end = '' )

			print( ' -> ', end = '' )

			first = True
			for species, coefficient in reaction.products.iteritems():
				to_print = []
				plus_sign = " + "
				if( first ):
					plus_sign = ""
					first = False

				to_print.add( plus_sign )
				to_print.add( str( coefficient ) )
				to_print.add( str( species ) )

				print( ''.join( to_print ), end = '' )

			print( '', end = '\n' ) # done printing the reaction, start new line


