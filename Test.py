from CRN import CRN
from Errors import FileFormatError

def main():
	try:
		crn = CRN('testfile.txt')
		crn.crn_print('crn_output.txt', False)
		crn.diff_eq_print('diff_eq_output.txt', False)
	except IOError as e:
		print('IOError: ' + str(e))
	except FileFormatError as e:
		print('FileFormatError: ' + str(e))

if __name__ == '__main__':
	main()
