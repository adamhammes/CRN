from CRN import CRN
from Errors import FileFormatError

def main():
	try:
		crn = CRN( eq_text = 'equations.txt' )
		for spec in crn.Species:
			print( spec )
	except FileFormatError as e:
		print('FileFormatError: ' + str(e))

if __name__ == '__main__':
	main()
