"""Module containing all Item classes."""

from general_funcs import print_line
import json


def all_items():
    """Get a list of all items available in game.

    Returns:
    items -- list of all items
    """
    with open('items.json') as i:
        items = [item for item in json.loads(i.read())]
    return items


class Item(object):
    """Item class. Only used for on-the-fly cases, not storage."""

    def __init__(self, name):
        """Item constructor.

        Arguments:
        name -- name of item
        """
        # Just needs to get the name, all other attributes are automatically
        # assigned by the following lines, from parsing an item.json file.
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
            inventory[item] += 1
            print_line(item)
        print_line("have been added to your inventory")

        chance = randint(0, 101)
        if (player.scrapper) * 3 > chance:
            print_line(
                "Your scrapper skill has allowed you to gain more components!")
            # Randomly adds extra component of the scrapped item the inventory.
            inventory[self.components[randint(len(self.components))]] += 1
        self.destroy("player")

    def destroy(self, target_inventory):
        """Remove item from inventory.

        Arguments:
        target_inventory -- inventory to remove Item from
        """
        if target_inventory == "player":
            global inventory
            for x in range(len(inventory)):
                if inventory[x].name == self.name:
                    inventory.remove(inventory[x])
                    break
        elif target_inventory == "trader":
            global trader_inventory
            for x in range(len(trader_inventory)):
                if trader_inventory[x].name == self.name:
                    trader_inventory.remove(trader_inventory[x])
                    break


class Inventory(dict):
    """Inventory class, inherits dict attributes."""

    def __init__(self, items=[]):
        """Inventory class constructor, sets values to 0."""
        for item in items:
            self[item] = 0

    def print(self):
        """Print all items in inventory."""
        att = " | {}: {}"
        for item in self:
            if self[item] > 0:
                print_line("{} * {}".format(item, self[item]), end="")
                print_line(att.format("Weight", Item(item).weight), end="")
                print_line(att.format("Value", Item(item).value), end="")
                print_line(att.format("Rarity", Item(item).rarity), end="")
                print_line(att.format("Components", Item(item).components))
                # maybe use align_text() for this?
