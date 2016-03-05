"""Module containing Room class."""

from general_funcs import print_line
from Item import Item
import json
import os
import sys

def all_rooms():
    """Get a list of all rooms in game.

    Returns:
    rooms -- list of all rooms
    """
    fn = "rooms.json"
    path = os.path.join(os.path.dirname(sys.argv[0]), fn)
    with open(path) as r:
        rooms = [room for room in json.loads(r.read())]
    return rooms


class Room(object):  # Basic class for the rooms in the game.
    """Room class."""

    def __init__(self, name, player):
        """Room class constructor.

        Arguments:
        name -- name of room
        player -- ???
        """
        self.name = name
        self.level = 1
        self.power_available = True
        with open('rooms.json') as f:
            parsed = json.loads(f.read())
            try:
                room = parsed[self.name]
                self.risk = room['risk']
                self.can_produce = room['can_produce']
                self.assigned_limit = room['assigned_limit']
                self.components = room['components']
                self.power_usage = room['power_usage']
                self.wattage = room['power_usage']
            except KeyError:
                print("Unknown item. Please contact dev.")
        self.assigned = []
        self.broken = False

        if self.can_produce:
            self.production = 0
            self.can_rush = True
        else:
            self.can_rush = False
        self.rushed = False
        
    def __str__(self):
        """String representation of object.

        Returns:
        self.name -- eg. "Living Room"
        """
        return "{} Room".format(self.name.title())

    def print_(self, game):
        """Print room name and its attributes.
        
        Arguments:
        game -- Main game object. Passes this to Room.update_production method
        """
        print_line(self)
        if self.power_available:
            power_availablility = "Working"
        else:
            power_availablility = "No power available"
        if self.broken:
            status = "Broken"
            status = "Functional"
        else:
            status = "Functional"
        print_line("    Risk: {}%".format(self.risk),
                   "    Level: {}".format(self.level),
                   "    Power: {}".format(power_availablility),
                   "    Status: {}".format(status))
        if self.can_produce:
            self.update_production(game.player)
            print_line("    Production: {}".format(self.production))
        if self.can_produce or self.name == "trader":
            print_line("    Assigned: ")
            self.see_assigned()
        print()

    def rush(self):
        """Rush building of Room."""
        self.rushed = 1  # Lets game know this room has been rushed.
        self.risk += 5
        print_line("{} has been rushed!".format(self.name))

    def fix(self):
        """Repair room if damaged."""
        global rooms

    def count_assigned(self):
        """Count inhabitants assigned to Room."""
        count = len(self.assigned)
        return count

    def see_assigned(self):
        """Print names of inhabitants assigned to Room."""
        if self.assigned:
            for person_name in self.assigned:
                print_line("        " + person_name)
        else:
            print_line("        None")

    def count_component(self, component):
        """Count components required to build Room.

        Arguments:
        component -- component to count

        Returns:
        int -- amount of component required to build Room
        """
        return self.components.count(str(component))

    def use_power(self):
        """Consume player's power."""
        for x in range(0, self.power_usage):
            Item('watt').destroy("player")
