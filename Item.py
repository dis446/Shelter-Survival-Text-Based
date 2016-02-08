class Item(object):

    def __init__(self, name):
        # Just needs to get the name, all other attributes are automatically
        # assigned by the following lines.
        self.name = name
        if self.name == "wood":
            self.value = 10
            self.weight = 5
            # This is a basic item and cannot be scrapped.
            self.components = []
            self.rarity = 1  # Determines chance of it showing up during scavenging or in the trader's inventory
        elif self.name == "steel":
            self.value = 50
            self.weight = 20
            self.components = []
            self.rarity = 4
        elif self.name == "turret":
            self.value = 200
            self.weight = 20
            self.components = [
                "steel",
                "steel",
                "steel",
                "chip",
                "steel",
                "steel"]
            self.rarity = 8
        elif self.name == "food":
            self.value = 20
            self.weight = 1
            self.components = []
            self.rarity = 2
        elif self.name == "water":
            self.value = 30
            self.weight = 2
            self.components = []
            self.rarity = 3
        elif self.name == "chip":
            self.value = 100
            self.weight = 1
            self.components = ["wire", "wire", "wire", "silicon"]
            self.rarity = 8
        elif self.name == "wire":
            self.value = 40
            self.weight = 3
            self.components = ['copper', 'copper', 'copper']
            self.rarity = 4
        elif self.name == "silicon":
            self.value = 50
            self.weight = 1
            self.components = []
            self.rarity = 6
        elif self.name == "copper":
            self.value = 20
            self.weight = 1
            self.components = []
            self.rarity = 3
        elif self.name == "gun":
            self.value = 100
            self.weight = 5
            self.components = ["steel", "copper"]
            self.rarity = 6
        elif self.name == "watt":
            self.value = 40
            self.weight = 0
            self.components = []
            self.rarity = 4

        else:
            print(
                "Item doesn't exist. Bug with item creation system. Please contact dev.")
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
