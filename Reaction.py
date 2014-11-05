
class Reaction:

	def __init__(self, rate_coeff, rate_var, reactants, products):
		self.rate_coeff = rate_coeff
		self.rate_var = rate_var
		self.reactants = reactants
		self.products = products
	
	def stoichiometry(self, species):
		return self.products.get(species, 0) - self.reactants.get(species, 0)
