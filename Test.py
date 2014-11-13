from CRN import CRN
from Errors import FileFormatError


def main():
	try:
		crn = CRN( eq_text = 'equations.txt' )
		crn.crn_print( file_name = 'crn_output.txt' )
	except FileFormatError as e:
		print('FileFormatError: ' + str(e) )

if __name__ == '__main__':
	main()
