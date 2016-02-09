from Human import Human
class Player(Human):
	def __init__(self,):
		Human.___init__(self, first_name, day_of_birth, parent_1, parent_2, age, gender)
		self.medic = 0  # Improves healing capabilities of stimpacks
		self.crafting = 0 # Chance to hold on to some components when crafting.
		self.tactician = 0  # Boosts defense
		self.cooking = 0  # Boosts production level of kitchen.
		self.barter = 0  # Decreases prices when buying, increases while selling. Goes up to 4
		self.inspiration = 0 # Boosts production and defense of all inhabitants.
		self.scrapper = 0 # Boosts chance of finding a component twice during scrapping.
		self.electrician = 0  # Boosts power production
