class Room(object):  # Basic class for the rooms in the game.

    def __init__(self, name):
        self.name = name
        # 1s and 0s that are used to store the indexes of assigned. Eg 001001
        # means that the 3rd and the 6th characters have been assigned here.
        self.assigned = ''
        # Determines the production level, max assigned limit etc.
        self.level = 1
        self.risk = 0  # Risk of breaking down, when rushed.
        self.broken = 0
        # 'On' if there is enough power for the room, 'Off' otherwise.
        self.power_available = "On"
        # Living rooms have no "assigned". Number of living rooms just limits
        # the total population of the shelter.
        if self.name == "living":
            # Stores whether or not room actually produces anything.
            # self.components=["wood",] #Need to add components.
            self.can_produce = 0
            self.assigned_limit = 0  # No-one can be assigned to the living room
            self.components = ["wood", "wood", "wood",
                               "wood"]  # Required to build this room
            self.power_usage = 5
        elif self.name == "generator":
            self.risk = 2
            self.can_produce = 1
            self.components = ["steel", "steel", "steel", "steel"]
            # Max number of workers that can work in the room at one time.
            self.assigned_limit = 3
            self.power_usage = 0
        elif self.name == "storage":
            self.can_produce = 0
            self.assigned_limit = 0
            self.components = ["steel", "steel"]
            self.power_usage = 1
        elif self.name == "kitchen":
            self.risk = 1
            self.can_produce = 1
            self.assigned_limit = 3
            self.components = ["wood", "wood", "wood"]
            self.power_usage = 10
        elif self.name == "trader":
            self.can_produce = 0
            self.assigned_limit = 1
            self.components = ["wood", "wood", "steel", "steel", "wood"]
            self.power_usage = 2
        elif self.name == "water works":
            self.risk = 2
            self.can_produce = 1
            self.assigned_limit = 3
            self.components = ["wood", "wood", "steel"]
            self.power_usage = 10
        elif self.name == "radio":
            self.can_produce = 0
            self.assigned_limit = 2
            self.components = ["wood", "wood", "steel", "steel", "wood"]
            self.power_usage = 15
        # Need to add more names.
        else:
            print(
                "Bug with room creation system. Please contact dev. Class specific bug.")
        if self.can_produce == 1:
            self.production = 0
            self.can_rush = 1
            self.rushed = 0
        else:
            self.can_rush = 0

    def rush(self):
        global rooms
        self.rushed = 1  # Lets game know this room has been rushed.
        self.risk += 5
        print(self.name, " has been rushed!")

    def fix(self):
        global rooms
    """#Old assignment string management system.
	def update_assigment(): #Updates length of assigned variable, due to population growth, by adding more zeros to it.
		global rooms
		current_count=len(self.assigned) #Count's how many digits exist
		required_count=len(people) #Count's how many digits should exists
		difference=required_count-current_count
		for x in range(difference):
			self.assigned.append('0') #Adds a zero at the end of the string based on the total population.
	"""

    # Calculates production level based on number, and skills, of assigned
    # people.
    def update_production(self):
        global rooms
        if self.broken == 1:
            self.production = 0
            print(self.name, "is broken and needs to be fixed.")
        else:
            player = people[0]  # Fetches player so their stats can be used.
            self.production = 0
            if self.name == "generator":
                for person_index in str(self.assigned):
                    if person_index == '1':
                        self.production += (people[int(person_index)
                                                   ].strength) * 10
                if player.electrician > 0:
                    self.production = self.production * \
                        (1 + (player.electrician * 0.05))

            elif self.name == "kitchen":
                for person_index in str(self.assigned):
                    if person_index == '1':
                        self.production += (people[int(person_index)
                                                   ].intelligence) * 10
                if player.cooking > 0:
                    self.production = self.production * \
                        (1 + (player.cooking * 0.05))

            elif self.name == "water works":
                for person_index in str(self.assigned):
                    if person_index == '1':
                        self.production += (people[int(person_index)
                                                   ].perception) * 10
                if player.cooking > 0:
                    self.production = self.production * \
                        (1 + (player.cooking * 0.05))
            elif self.name == "radio":
                for person_index in str(self.assigned):
                    if person_index == '1':
                        self.production += (people[int(person_index)
                                                   ].charisma) * 10
                if player.inspiration > 0:
                    self.production = self.production * \
                        (1 + (player.inspiration * 0.05))
            else:
                print("Bug with room production update system. Please contact dev.")
            if player.inspiration > 0:
                self.production = self.production * \
                    (1 + (player.inspiration * 0.03))
            if self.can_rush == 1 and self.rushed == 1:
                self.production = self.production * 2

    def upgrade(self):
        global rooms
        if self.can_produce == 1:
            self.production += 20
            self.assigned_limit += 2
        self.level += 1

    def count_assigned(self):
        count = 0
        for x in str(self.assigned):
            if x == '1':
                count += 1
        return count

    def see_assigned(self):
        count = 0
        for x in str(self.assigned):
            if x == '1':
                person = people[count]
                print("      ", person.name, person.surname)
            count += 1

    def count_component(self, component):
        return self.components.count(str(component))

    def can_use_power(self):
        if count_item('watt', 'player') > self.power_usage:
            return True
        else:
            return False

    def use_power(self):
        for x in range(0, self.power_usage):
            Item('watt').destroy("player")
