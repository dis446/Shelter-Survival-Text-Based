class Human(object):  # Basic class for all the Humans present in the game.
	def __init__(self, first_name, day_of_birth, parent_1, parent_2, age, gender):
		self.name = first_name #First name
		self.day_of_birth = day_of_birth
		self.parent_1 = parent_1  # Surname
		self.parent_2 = parent_2  # Surname
		self.gender = gender
		self.surname = self.parent_1 
		self.partner = "" 
		
		# The stats of the person. Affects the production of
		# room the person has been assigned to.
		self.strength = 1
		self.perception = 1
		self.endurance = 1
		self.charisma = 1
		self.intelligence = 1
		self.luck = 1

		self.assigned_room = ""  # Keeps track of where person is working.
		self.can_mate = False  # Keeps track of mating ablility
		self.children = []  # List of all children
		self.partner = "" # Keeps track of partner of person. Only partners can have coitus.
		self.level = 1 #Determines production 
		self.XP = 0

	def gain_xp(self, amount):
		self.XP += amount

	def level_up(self):
		see_stats(self.name, self.surname)
		self.level += 1
		if self.name == people[0].name:  # If player has leveled up
			print("\n")
			choice = input("Please choose an attribute to level up: ")
			choice.lower()
			if choice == "strength":
				self.strength += 1
			elif choice == "perception":
				self.perception += 1
			elif choice == "endurance":
				self.endurance += 1
			elif choice == "charisma":
				self.charisma += 1
			elif choice == "intelligence":
				self.intelligence += 1
			elif choice == "luck":
				self.luck += 1
			elif choice == "medic":
				self.medic += 1
			elif choice == "crafting":
				self.crafting += 1
			elif choice == "tactitian":
				self.tactitian += 1
			elif choice == "cooking":
				self.cooking += 1
			elif choice == "inspiration":
				self.inspiration += 1
			elif choice == "scrapper":
				self.scrapper += 1
			elif choice == "barter":
				self.barter += 1
			elif choice == "electrician":
				self.electrician += 1
			else:
				print("Invalid choice")
				self.level -= 1
				self.level_up()
		else:  # If NPC has levelled up
			if choice == "strength":
				self.strength += 1
			elif choice == "perception":
				self.perception += 1
			elif choice == "endurance":
				self.endurance += 1
			elif choice == "charisma":
				self.charisma += 1
			elif choice == "intelligence":
				self.intelligence += 1
			elif choice == "luck":
				self.luck += 1
			else:
				print("'\nInvalid choic.\n")
				self.level -= 1
				self.level_up()

	def mature(self):
		self.age += 1
		print(self.name, " has matured and is now ", self.age, " years old!")

	def take_damage(self, amount):
		self.defense = self.strength * 10
		damage_taken = amount - self.defense
		if damage_taken < 1:
			damage_taken = 0
		else:
			self.HP -= damage_taken
			if self.HP < 1:
				self.die()

	def heal(self, amount):
		player = people[0]
		if player.medic > 0:  # Medic Boost.
			amount = amount * (1 + (0.05 * player.medic))
		self.HP += amount
		if self.HP > 99:  # Truncates health
			self.HP = 100

	def rebirth(self):  # Don't know if I'll ever use this.
		self.age = 0
		if self.gender == "f":
			print(self.name, " has been reborn and his stats have been reset")
		else:
			print(self.name, " has been reborn and her stats have been reset")
		self.strength = 1
		self.perception = 1
		self.endurance = 1
		self.charisma = 1
		self.intelligence = 1
		self.luck = 1

	def get_index(self):  # Returns the index of the character in the people list
		for x in range(len(people)):
			if people[x].name == self.name and people[
					x].surname == self.surname:
				return int(x)

	def unassign(self):
		for room in rooms:  # Breaks apart each room's assigned number, removes the person, and reassembles the assigned number.
			string_room_name = str(room.assigned)
			lst = []
			for digit in string_room_name:
				lst.append(digit)
			lst[person_index] = '0'
			string = ''
			for digit in lst:
				string = string + digit
			room.assigned = string
		self.assigned_room = ''

	def assign_to_room(self, chosen_room):
		global rooms
		global people
		person_index = self.get_index()
		#print("Index of ",self.name,"is",person_index)
		room_index = get_room_index(chosen_room)
		#print("Index of ",chosen_room," is ",room_index)
		room = rooms[room_index]  # Refers to the actual room
		#print("Chosen room is",room.name)
		if people[
				person_index].assigned_room != '':  # If person has been assigned before
			for room in rooms:
				string = str(room.assigned)
				lst = []
				for digit in string:
					lst.append(digit)
				lst[person_index] = '0'
				string = ''
				for digit in lst:
					string = string + digit
				room.assigned = string
		string = str(room.assigned)
		#print("Assigned log",string)
		lst = []
		for digit in string:
			lst.append(digit)
		#print("Assigned log",lst)
		lst[person_index] = '1'
		string = ''
		for digit in lst:
			string = string + digit
		room.assigned = string
		#print("Updated assigned log",room.assigned)
		# Let's  character know where they've been assigned.
		people[person_index].assigned_room = str(chosen_room)
		#print("Room",self.name,"has been assigned to is",people[person_index].assigned_room)
		print(self.name, self.surname, "has been assigned to", chosen_room)

	# Checks if person can have coitus and have children. Perfomed twice when
	# player inputs coitus, once for each proposed parent.
	
	def can_mate_check(self):
		self.can_mate = True
		if self.age < 18:
			self.can_mate = False
		if len(self.children) > 5:  # Upper limit of children is 5
			self.can_mate = False
		# Have to wait for a year before parent can have child again.
		for child in self.children:
			if people(child).age < 1:
				self.can_mate = False

	
