from CRN import CRN

def main():
  crn = CRN('testfile.txt')
  crn.crn_print('crn_output.txt')
  crn.diff_eq_print('diff_eq_output.txt')
