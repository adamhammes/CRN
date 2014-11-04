
# returns a complex with the following format:
def line_reader( species, line ):
	terms = line.split(' ')
	terms = [item for item in list if item]

	rate_constant = terms[0]

	num = 0;
	sign = 1

	i = 0
	if( rate_constant[0] == '-'):
		sign = -1
		i += 1

	while( rate_constant[i].isdigit() ):
		num *= 10
		num += rate_constant[i]
		i += 1

	num *= sign