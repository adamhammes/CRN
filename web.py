from flask import Flask, request, render_template
from CRN import CRN
from Errors import FileFormatError

app = Flask( __name__ )

@app.route('/', methods = ['GET', 'POST'])
def index():
	input_text = ''
	crn_text = ''
	if request.method == 'POST':
		input_text = request.form['equations']
		try:
			crn = CRN( eq_text = input_text.split( '\n' ) )
			crn_text = str( crn )
		except FileFormatError as e:
			crn_text = 'Error:\n' + str(e)

	return render_template( 
		'gui_template.html',
		crn_input = input_text,
		crn_output = crn_text )

if __name__ == '__main__':
	app.run()