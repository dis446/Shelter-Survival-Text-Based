from Human import Human
class NPC(Human):
	def __init__(self, first_name, day_of_birth, parent_1, parent_2, age, gender):
		Human.___init__(self, first_name, day_of_birth, parent_1, parent_2, age, gender)
		self.scavenging = False
		self.days_scavenging = 0
		self.days_to_scavenge_for = 0
	def die(self):
		global people
		global rooms
		print(self.name, " has died")
		# Uses first index since player will always be the first person in the
		# list, checks if player has died.
		end = 1  # Ends game since player has died.
		if self.assigned_room != "":  # Deals with if the person was assigned to any rooms.
			for x in range(people):  # Fetches the index of the person.
				if people[x].name == self.name:
					index = x
					break
			for r in rooms:
				# Removes person from the rooms' assigned records.
				del r.assigned[index]
		people.remove(self)
