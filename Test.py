# -*- coding: utf-8 -*- 

from CRN import CRN
from Errors import FileFormatError

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def main():
	string = [u"x' = − 2αx^2v + 2γz^4", u"y' = 3αx^2v − 3βy^3v^2", u"z' = 4βy^3v^2 − 4γz^4", "v' = αx2^v − 2βy^3v^2 + γz^4"]
	
	crn = CRN( eq_text = string)


if __name__ == '__main__':
	main()
