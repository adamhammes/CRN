from CRN import CRN

def main():
  crn = CRN( gui_text = 'testfile.txt')
  crn.crn_print( file_name = 'crn_output.txt')
  crn.diff_eq_print( file_name = 'diff_eq_output.txt')
