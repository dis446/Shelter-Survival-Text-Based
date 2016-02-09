class Item(object):

	def __init__(self, name):
		# Just needs to get the name, all other attributes are automatically
		# assigned by the following lines.
		self.name = name
		with open('items.json') as f:
		    parsed = json.loads(f.read())
		    try:
		        item = parsed[self.name]
		        self.value = item['value']
		        self.weight = item['weight']
		        self.components = item['components']
		        self.rarity = item['rarity']
		    except KeyError:
		        print("Unknown item. This is a bug. Please contact the dev.")
		# Keeps track of whether item has been scrapped by player.
		self.scrapped = 0

	def count_component(self, component):
		return self.components.count(str(component))

	# Destroys the item and adds it's compoenents to the inventory.
	def scrap(self):
		global inventory
		print(self.name, " has been scrapped and these")
		for item in self.components:
			inventory.append(item)
			print(item)
		print("have been added to your inventory")

		chance = randint(0, 101)
		if (people[0].scrapper) * 3 > chance:
			print("You scrapper skill has allowed you to gain more components!")
			for item in self.components:
				inventory.append(item)
		self.scrapped = 1  # Differentiate between whether item has been scrapped or just destroyed
		self.destroy("player")

	def destroy(self, target_inventory):
		global inventory
		if target_inventory == "player":
			for x in range(len(inventory)):
				if Item(inventory[x]).name == self.name:
					inventory.remove(inventory[x])
					break
		elif target_inventory == "trader":
			global trader_inventory
			for x in range(len(trader_inventory)):
				if Item(trader_inventory[x]).name == self.name:
					trader_inventory.remove(trader_inventory[x])
					break
	#	if self.scrapped!=1: #Don't need to print anything if the item has been scrapped
	#		print(self.name," has been used!")
