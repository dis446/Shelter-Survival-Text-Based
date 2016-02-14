"""Module containing Room class."""

from general_funcs import print_line
from Item import Item
import json


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
            except KeyError:
                print("Unknown item. Please contact dev.")
        self.assigned = []
        self.broken = False

        if self.can_produce:
            self.production = 0
            self.can_rush = True
            self.rushed = False
        else:
            self.can_rush = False

    def __str__(self):
        """String representation of object.

        Returns:
        self.name -- eg. "Living Room"
        """
        return "{} Room".format(self.name.title())

    def rush(self):
        """Rush building of Room."""
        global rooms
        self.rushed = 1  # Lets game know this room has been rushed.
        self.risk += 5
        print_line(self.name, " has been rushed!")

    def fix(self):
        """Repair room if damaged."""
        global rooms

    def update_production(self, player):
        """Calculate production value of Room.

        Arguments:
        player -- player object
        """
        if self.broken:
            production = 0
            print_line(self.name, "is broken and needs to be fixed.")
        else:
            production = 0
            if self.name == "generator":
                for person_index in str(self.assigned):
                    if person_index == '1':
                        production += people[int(person_index)].strength * 10
                if player.electrician > 0:
                    production = production * (1 + (player.electrician * 0.05))
            elif self.name == "kitchen":
                for person_index in str(self.assigned):
                    if person_index == '1':
                        production += people[int(person_index)].intelligence \
                            * 10
                if player.cooking > 0:
                    production = production * \
                        (1 + (player.cooking * 0.05))

            elif self.name == "water works":
                for person_index in str(self.assigned):
                    if person_index == '1':
                        production += people[int(person_index)].perception * 10
                if player.cooking > 0:
                    production = production * \
                        (1 + (player.cooking * 0.05))
            elif self.name == "radio":
                for person_index in str(self.assigned):
                    if person_index == '1':
                        production += people[int(person_index)].charisma * 10
                if player.inspiration > 0:
                    production = production * \
                        (1 + (player.inspiration * 0.05))
            else:
                print_line(
                    "Bug with room production update system.",
                    "Please contact dev.")
            if player.inspiration > 0:
                production = production * \
                    (1 + (player.inspiration * 0.03))
            if self.can_rush and self.rushed:
                production = production * 2
            return production

    def count_assigned(self):
        """Count inhabitants assigned to Room."""
        count = 0
        for x in str(self.assigned):
            if x == '1':
                count += 1
        return count

    def see_assigned(self):
        """Print names of inhabitants assigned to Room."""
        count = 0
        for x in str(self.assigned):
            if x == '1':
                person = people[count]
                print_line("      ", person.name, person.surname)
            count += 1

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