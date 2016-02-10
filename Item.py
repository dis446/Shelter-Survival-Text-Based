"""Module containing all Item classes."""

from general_funcs import print_line
import json


class Item(object):
    """Item class. Only used for on-the-fly cases, not storage."""

    def __init__(self, name):
        """Item constructor.

        Arguments:
        name -- name of item
        """
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
                print_line(
                    "Unknown item. This is a bug. Please contact the dev.")
        # Keeps track of whether item has been scrapped by player.
        self.scrapped = False

    def count_component(self, component):
        """Count number of components in Item.

        Arguments:
        component -- component to count
        """
        return self.components.count(str(component))

    def scrap(self):
        """Destroy Item and add its components to inventory."""
        global inventory
        print_line(self.name, " has been scrapped and these")
        for item in self.components:
            inventory.append(item)
            print_line(item)
        print_line("have been added to your inventory")

        chance = randint(0, 101)
        if (people[0].scrapper) * 3 > chance:
            print_line(
                "Your scrapper skill has allowed you to gain more components!")
            for item in self.components:
                inventory.append(item)
        self.scrapped = True  # whether item is scrapped or just destroyed
        self.destroy("player")

    def destroy(self, target_inventory):
        """Remove item from inventory.

        Arguments:
        target_inventory -- inventory to remove Item from
        """
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
    #    if self.scrapped!=1:
    #        print_line(self.name," has been used!")
