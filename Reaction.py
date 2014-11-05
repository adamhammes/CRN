
class Reaction:

	def __init__(self, rate, reactants, products):
		self.rate = rate
		self.reactants = reactants
		self.products = products
	
	def stoichiometry(self, species):
		return self.products.get(species, 0) - self.reactants.get(species, 0)
