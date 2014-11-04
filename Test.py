from CRN import CRN

def main():
  crn = CRN( gui_txt = 'testfile.txt')
  crn.crn_print( file_name = 'crn_output.txt')
  crn.diff_eq_print( file_name = 'diff_eq_output.txt')

if __name__ == '__main__':
	main()
