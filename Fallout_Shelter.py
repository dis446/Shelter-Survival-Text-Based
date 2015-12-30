#Text-based Fallout Shelter game developed by T.G. and The-9880.
from random import randint
from time import sleep
import sys
try:
	from tqdm import tqdm #Used to make loading screens.
except ImportError:
	print("Error importing TQDM module. The game will still run regardless, but if this module was present, the game would be slightly better.")
"""#Function to space out prints, giving player time to read. Similar to Fallout 4 terminall CLI.	
def printl(a):
	sleep(0.5)
	print(str(a))
def  printl(a,b):
	printl(a)
	printl(b)
def printl(a,b,c):
	printl(a)
	printl(b)
	printl(c)
def printl(a,b,c,d):
	printl(a)
	printl(b)
	printl(c)
	print(d)
def printl(a,b,c,d,e):
	printl(a)
	printl(b)
	printl(c)
	print(d)
	print(e)
def printl(a,b,c,d,e,f):
	printl(a)
	printl(b)
	printl(c)
	print(d)
	print(e)
	print(f)
"""

class Human(object): #Basic class for all the Humans present in the game.
	def __init__(self,name,day_of_birth,parent_1,parent_2,gender):
		self.name=name
		self.day_of_birth=day_of_birth
		self.parent_1=parent_1
		self.parent_2=parent_2
		self.gender=gender
		if len(all_people) <6 and day_count<3: #First 5 people will be 21 years old, so they can mate.
			self.age=21
		else:
			self.age=0
		if len(all_people)<6: #Early inhabitants just adopt their father's first names as surnames.
			self.surname=self.parent_1
		else: #Futher inhabitants inherit the family name
			parent_1_index=get_person_index(self.parent_1)
			self.surname=all_people[parent_1_index].surname
			
		if len(all_people)==0: #Stats specific to the player
			self.medic=0 #Improves healing capabilities of stimpacks
			self.crafting=0 #Chance to hold on to some components when crafting.
			self.tactitian=0 #Boosts defense
			self.cooking=0 #Boosts production level of kitchen.	
			self.barter=0 #Decreases prices when buying, increases while selling. Goes up to 4
			self.inspiration=0 #Boosts production and defense of all inhabitants.
			self.scrapper=0 #Boosts chance of finding a component twice during scrapping.
			self.electrician=0 #Boosts power production
			self.assigned_room=""
		else: #Stats specific to NPCs
			self.scavenging = 0
			self.daysScavenging = 0
			self.daysToScavengeFor = 0
			self.assigned_room="" #Keeps track of where person is working.
		
		self.hunger=0
		self.thirst=0
		self.HP=100
		#The stats of the person. Plan to use this to affect the production of room the person has been assigned to.
		self.strength=1
		self.perception=1
		self.endurance=1
		self.charisma=1
		self.intelligence=1
		self.luck=1
		
		self.can_mate=0 #Keeps track of mating ablility
		self.children=[] #List of all children
		self.partner="" #Keeps track of partner of person. Only partners can have coitus.
		self.level=1
		self.XP=0
	def see_stats(self): #View stats of person.
		print("Strength: ",self.strength)
		print("Perception: ",self.perception)
		print("Endurance: ",self.endurance)
		print("Charisma: ",self.charisma)
		print("Intelligence: ",self.intelligence)
		print("Luck: ",self.luck)
		if self.name==all_people[0].name: #Player has extra stats
			print("")
			print("Medic: ",self.medic)
			print("Crafting: ",self.crafting)
			print("Tactitian: ",self.tactitian)
			print("Cooking: ",self.cooking)
			print("Inspiration: ",self.inspiration)
			print("Scrapping: ",self.scrapper)
			print("Bartering: ",self.barter)
			print("Electricain: ",self.electrician)
	def gain_xp(self,amount):
		self.XP+=amount
	def level_up(self):
		self.see_stats()
		self.level+=1
		if self.name==all_people[0].name: #If player has leveled up
			choice=input("Please choose an attribute to level up: ")
			choice.lower()
			if choice=="strength":
				self.strength+=1
			elif choice=="perception":
				self.perception+=1
			elif choice=="endurance":
				self.endurance+=1
			elif choice=="charisma":
				self.charisma+=1
			elif choice=="intelligence":
				self.intelligence+=1
			elif choice=="luck":
				self.luck+=1
			elif choice=="medic":
				self.medic+=1
			elif choice=="crafting":
				self.crafting+=1
			elif choice=="tactitian":
				self.tactitian+=1
			elif choice=="cooking":
				self.cooking+=1
			elif choice=="inspiration":
				self.inspiration+=1
			elif choice=="scrapper":
				self.scrapper+=1
			elif choice=="barter":
				self.barter+=1
			elif choice=="electrician":
				self.electrician+=1
			else:
				print("Invalid choice")
				self.level-=1
				self.level_up()
		else: #If NPC has levelled up
			if choice=="strength":
				self.strength+=1
			elif choice=="perception":
				self.perception+=1
			elif choice=="endurance":
				self.endurance+=1
			elif choice=="charisma":
				self.charisma+=1
			elif choice=="intelligence":
				self.intelligence+=1
			elif choice=="luck":
				self.luck+=1
			else:
				print("Invalid choice")
				self.level-=1
				self.level_up()
		
		
	def mature(self):
		self.age+=1
		print(self.name," has matured and is now ",self.age," years old!")
	def take_damage(self,amount):
		self.defense=self.strength*10
		damage_taken=amount-self.defense
		if damage_taken<1:
			damage_taken=0
		else:	 
			self.HP-=damage_taken
			if self.HP < 1:
				self.die()
	def heal(self,amount):
		player=all_people[0]
		if player.medic>0: #Medic Boost.
			amount=amount*(1+(0.05*player.medic))
		self.HP+=amount
		if self.HP>99: #Truncates health
			self.HP=100
	def rebirth(self): #Don't know if I'll ever use this.
		self.age=0
		if self.gender=="f":	
			print(self.name," has been reborn and his stats have been reset")
		else:
			print(self.name," has been reborn and her stats have been reset")
		self.strength=1
		self.perception=1
		self.endurance=1
		self.charisma=1
		self.intelligence=1
		self.luck=1
		
	def get_index(self): #Returns the index of the character in the all_people list
			for x in range(len(all_people)):
				if all_people[x].name==self.name and all_people[x].surname==self.surname:
					return int(x)
				
	def assign_to_room(self,chosen_room):
		global rooms
		global all_people
		person_index=self.get_index()
		#print("Index of ",self.name,"is",person_index)	
		room_index=get_room_index(chosen_room)
		#print("Index of ",chosen_room," is ",room_index)
		room=rooms[room_index]#Refers to the actual room
		print("Chosen room is",room.name)
		if all_people[person_index].assigned_room!='': #If person has been assigned before
			for room in rooms:
				string=str(room.assigned)
				lst=[]
				for digit in string:
					lst.append(digit)
				lst[person_index]='0'
				string=''
				for digit in lst:
					string=string+digit
				room.assigned=string
		string=str(room.assigned)
		#print("Assigned log",string)
		lst=[]
		for digit in string:
			lst.append(digit)
		#print("Assigned log",lst)
		lst[person_index]='1'
		string=''
		for digit in lst:
			string=string+digit
		room.assigned=string
		print("Updated assigned log",room.assigned)				
		all_people[person_index].assigned_room=str(chosen_room)#Let's  character know where they've been assigned.
		#print("Room",self.name,"has been assigned to is",all_people[person_index].assigned_room)
	def can_mate_check(self): #Checks if person can have coitus and have children. Perfomed twice when player inputs coitus, once for each proposed parent.
		self.can_mate=1
		if self.age <18:
			self.can_mate=0
		if len(self.children)>5: #Upper limit of children is 5
			self.can_mate=0
		for child in self.children: #Have to wait for a year before parent can have child again.
			if all_people(child).age<1:
				self.can_mate=0
	def die(self): 
		global end
		global all_people
		global rooms
		print(self.name," has died")
		if all_people[0].name==self.name: #Uses first index since player will always be the first person in the list, checks if player has died.
			end=1 #Ends game since player has died.
		if self.assigned_room!="": #Deals with if the person was assigned to any rooms.
			for x in range(all_people): #Fetches the index of the person.
					if all_people[x].name==self.name:
						index=x
						break
			for r in rooms:
				del r.assigned[index] #Removes person from the rooms' assigned records.
		all_people.remove(self)
		
		
		
		
class Room(object): #Basic class for the rooms in the game.
	def __init__(self,name): #Name would be something like "living_room_3" while group would be "living". So all living rooms have the same initial stats.
		self.name=name 
		self.assigned='' #1s and 0s that are used to store the indexes of assigned. Eg 001001 means that the 3rd and the 6th characters have been assigned here.
		self.level=1 #Determines production level, max assigned limit etc.
		self.risk=0
		if self.name=="living": # Living rooms have no "assigned". Number of living rooms just limits the total population of the shelter.
			self.can_produce=0 #Stores whether or not room actually produces anything.				self.components=["wood",] #Need to add components.
			self.assigned_limit=0 #No-one can be assigned to the living room
			self.components=["wood","wood","wood","wood"] #Required to build this room
		elif self.name=="generator":
			self.risk=2
			self.can_produce=1
			self.assigned_limit=4 #Max number of workers that can work in the room at one time.
		elif self.name=="storage":
			self.can_produce=0
			self.assigned_limit=0
		elif self.name=="kitchen":
			self.risk=2
			self.can_produce=1
			self.assigned_limit=5
			self.components=["wood","wood","wood"]
		elif self.name=="trader":
			self.can_produce=0
			self.assigned_limit=1
			self.components=["wood","wood","wood","steel","wood"]
		else:	
			print("Bug with room creation system. Please contact dev. Class specific bug.")
		if self.can_produce==1:
			self.production=int(100)
			self.can_rush=1
			self.rushed=0
		# Need to add more names.	
		
	def rush(self): 
		global rooms
		if self.can_rush==0: #Method should never be called on non-rushable rooms.
			print("Bug with can_rush check. Please contact dev.")
		else:
			self.production+=50
			self.rushed=1 #Lets game know this room has been rushed.
			print(self.name, " has been rushed!")

#	def update_assigment(): #Updates length of assigned variable, due to population growth, by adding more zeros to it.
#		global rooms
#		current_count=len(self.assigned) #Count's how many digits exist
#		required_count=len(all_people) #Count's how many digits should exists
#			difference=required_count-current_count 
#			for x in range(difference):
#				self.assigned.append('0') #Adds a zero at the end of the string based on the total population.
		
	def update_production(self): #Calculates production level based on number of and skills of assigned. 
		global rooms
		if self.can_produce==0:
			print("Bug with room production update system. Please contact dev.")
		else:
			player=all_people[0] #Fetches player so his stats can be used.
			self.production=0 
			if self.name=="generator":
				for person_index in str(self.assigned):
					if person_index=='1':
						self.production+=all_people[person_index].intelligence
				if player.electrician >0:
					self.production=self.production*(1+(player.electrician*0.05))
			
			elif self.name=="kitchen":
				for person_index in str(self.assigned):
					if person_index=='1':
						self.production+=all_people[person_index].charisma
				if player.cooking >0:
					self.production=self.production*(1+(player.cooking*0.05)) 
			else:
				print("Bug with room production update system. Please contact dev.")
			if player.inspiration>0:
				self.production=self.production*(1+(player.inspiration*0.03))
				
	def upgrade(self):
		global rooms
		if self.can_produce==1:
			self.production+=20
			self.assigned_limit+=2
		self.level+=1
	def count_assigned(self):
		count=0
		for x in str(self.assigned):
			if x=='1':
				count+=1
		return count
	def see_assigned(self):
		index=0
		for x in str(self.assigned):
			if x=='1':
				person=all_people[index]
				print("Name : ",person.name)
			index+=1
	def count_component(self,component):
		count = 0
		for x in self.components:
			if x == component:
				count += 1
		return count
	
	
class Item(object): # Basic model for items in the game. Objects of this class will never be stored, instead created on the fly to retrieve attributes.
	def __init__(self,name):
		self.name=name#Just needs to get the name, all other attributes are automatically assigned by the following lines.
		if self.name=="wood":
			self.value=10
			self.weight=5
			self.components=[] #This is a basic item and cannot be scrapped.
			self.rarity=1 #Determines chance of it showing up during scavenging or in the trader's inventory
		elif self.name=="steel":
			self.value=50
			self.weight=20
			self.components=[]
			self.rarity=3
		elif self.name=="turret":
			self.value=200
			self.weight=20
			self.components=["steel","steel","steel","electronic chip"]
			self.rarity=7
		elif self.name=="food":
			self.value=20
			self.weight=1
			self.components=[]
			self.rarity=3
		elif self.name=="water":
			self.value=30
			self.weight=2
			self.components=[]
			self.rarity=3
		elif self.name=="electronic chip":
			self.value=100
			self.weight=1
			self.components=["wire","wire","wire","silicon"]
			self.rarity=8
		elif self.name=="wire":
			self.value=40
			self.weight=1
			self.components=[]
			self.rarity=4
		elif self.name=="silicon":
			self.value=50
			self.weight=3
			self.components=[]
			self.rarity=6
		
		
			
		
		else:
			print("Item doesn't exist. Bug with item creation system. Please contact dev.")
		self.scrapped=0 #Keeps track of whether item has been scrapped by player.
	    
	def count_component(self,component):
		count = 0
		for x in self.components:
			if x == component:
				count += 1
		return count
		
	def scrap(self): #Destroys the item and adds it's compoenents to the inventory.
		global inventory
		print(self.name," has been scrapped and these")
		for item in self.components:
			inventory.append(item)
			print(item)
		print("have been added to your inventory")
		
		chance=randint(0,101)
		if (all_people[0].scrapper)*3>chance:
			print("You scrapper skill has alllowed you to gain more components!")	
			for item in self.components:
				inventory.append(item)
		self.scrapped=1 #Differentiate between whether item has been scrapped or just destroyed
		self.destroy()
	
	def destroy(self):
		global inventory
		for x in range(len(inventory)):
			if Item(inventory[x]).name==self.name:
				inventory.remove(inventory[x])
				break
		if self.scrapped!=1: #Don't need to print anything if the item has been scrapped
			print(self.name," has been destroyed!")





#Information system!
# Bunch of functions used by other functions to retrieve information about the shelter, it's assigned, rooms and items.
load=0
def load_time(x,message):
	
	if 'tqdm' in sys.modules and load==1:
		print(str(message))
		for x in tqdm(range(0,x)):
			sleep(0.01)
	else:
		print(str(message))
		sleep(x/10000)	
def input_int(x): #Whenever player has to input an integer, this should be used. Catches errors.
	x=input("Input an integer.")
	try:
		int(x)
	except ValueError:
		print("Invalid. Only integer numbers are accepted!")
		x=input("Try again. Input:")
		check_int(x) #Recursion!
	return x

def count_item(item,target_inventory): #Counts total number of an item present in an inventory
	item=str(item)
	count=0
	if target_inventory=="player":
		for x in inventory:
			if x==item:
				count+=1
		return count
	elif target_inventory=="trader":
		for x in trader_inventory:
			if x==item:
				count+=1
		return count
	else:
		print("Bug with item counting system. Please contact dev!")
		
def count_weight(): #Calculates the sum of the weights of all items currently in the inventory,
	count=0
	for x in inventory:
		count+=Item(x).weight #Creates instances of class on the fly. If 5 wood present, tempoarily creates 5 wood, one by one, uses their weight and discards them
	return count
		
def storage_capacity(): #Calculates how much more weight the player can hold.  Used to check if player can take any more items.
	global all_rooms
	capacity=all_rooms("storage").production
	return capacity
		
def check_room(x): #Checks if the room exists
	for r in all_rooms:
		if x==r:
			return True
	return False
	
def check_built_room(x): #Checks if room has been built yet
	for r in rooms:
		if x==r.name:
			return True
	return False
			
def see_people(): #Displays everyone in the shelter.
	print("Name. Age. Gender. Hunger. Thirst. Assinged room")
	for person in all_people:
		print(person.name,person.parent_1,person.age,person.gender,person.hunger,person.thirst,person.assigned_room) #Need to add more attributes

def see_rooms():
	for r in rooms:
		print(r.name,". Risk: ",r.risk,". Level: ", r.level,". Assigned: ",r.see_assigned())
		
def see_inventory(inven):#Displays all items in inventory in the form (Log*5.Weight=5.Value=10.Components="Wood". Rarity=1).
	inven=str(inven)
	seen_items=[]
	if inven=="player":
		for x in inventory:
			if x not in seen_items:
				count=count_item(x,"player")
				if count>0: #If there are no instances of the item present, no need to display it.				
					it=Item(x) #Creates a tempoary object so it's data can be fetched.
					print(x,"*",count,". Weight: ",it.weight,". Value: ",it.value,". Components: ",it.components,". Rarity: ",it.rarity)
					seen_items.append(x)
	elif inven=="trader":
		for x in trader_inventory:
			if x not in seen_items:
				count=count_item(x,"trader")
				if count>0: #If there are no instances of the item present, no need to display it.				
					it=Item(x)
					print(x,"*",count,". Weight: ",it.weight,". Value: ",it.value,". Components: ",it.components,". Rarity: ",it.rarity)
					seen_items.append(x)
	else:			
		print("Major bug with inventory information system. Please contact dev!")
def living_capacity():
	index=get_room_index('living')
	room=rooms[index]
	capacity=0
	for x in range(room.level):
		capacity+=10
	return capacity
def see_resources():
	food_count=count_item("food","player")
	water_count=count_item("water","player")
	power_count=count_item("watt","player")
	print("Food * ",food_count)
	print("Water * ",water_count)
	print("Power * ",power_count)
def  get_person_index(first_name,surname):
	for x in range(len(all_people)):
		if all_people[x].name==first_name and all_people[x].surname==surname:
			return int(x)
def get_room_index(room):
	room=str(room)
	for r in range(0,len(rooms)):
		if rooms[r].name==room:
			print("Room index fetch returns,",r)
			return r		






#Scavenging system.
def scavenge(first_name,surname,var): #Sends people on a scavenging mission.
	#Need to modify function to accept (first name) and (surname)
	global all_people
	if not check_person(first_name,surname):
		print("Error with scavenging system. Please contact dev!")
	else:
		person=all_people[get_person_index(first_name,surname)]
		person.scavenging=1
		if var=="days": #If player chooses to send player for certain number of days, or until health drops below 20.
			print("How many days do you want to send this person out?")
			day_choice=input_int()
			person.daysToScavengeFor = day_choice 
		else:
			person.daysToScavengeFor= 100 #Their health will drop below 20 before 100 days, so this is fine.
	use_points(10)






#Construction system.
def build(r): #Builds a room once checks are done. Should append to (rooms) list.
	global rooms
	global inventory
	built_room=Room(str(r)) #creates a room. 
	rooms.append(built_room) #Stores the room in memory.
	load_time(5,("Building ",r))
	for y in built_room.components: #Does this for each component
		for x in inventory: 
			if y == x: #If it matches, delete this.
				x.destroy() 
				break #Ensures that only one instance of the item is removed for every one instance of the component.
	all_people[0].gain_xp(100)
	use_points(50)
def craft(x):#Crafts an item once checks are done. Just add the name of an item to the inventory name.
	global inventory
	load_time(5,("Crafting ",x))
	add_to_inven(x, 1, "player")
	#Perk bonuses
	a = Item(x)
	for x in range(0,5):
		if all_people[0].crafting==x:
			chance=x*2
			break
	for y in a.components:
		for x in inventory:
			if y == x:
				chance_game=randint(0,101)
				if chance_game>chance:
					inventory.remove(x)
				break #Ensures that only one instance of the item is referenced.
	all_people[0].gain_xp(a.rarity*10) 
	use_points(5)
	







#Human management system
def get_player_gender():#Asks player what gender they are.
	gender=input("Please choose a gender.(M/F)")
	if len(gender)>0:
		gender=gender[0].lower()
		if gender=="m" or gender=="f":
			return gender
		else:
			print("Invalid gender choice!")
			get_player_gender()
	else:
		print("No input detected!")
		get_player_gender()

def get_gender(): #Randomly generates a gender. For NPCs
	gender=randint(0,1)
	if gender==0:
		gender="m"
	else:
		gender="f"
	return gender
def check_person(first_name,surname): #Check if a person exists.
	for per in all_people:
		if per.name==first_name and per.surname==surname:
			print("This person exists")
			return True
	else:
		return False
def check_xp(name,surname):
	global all_people
	person_index=get_person_index(name,surname) #Fetches index of person in the all_people list.
	person=all_people[person_index] #Fetches person object and stores it locally. So now (person) is a shortcut to the person.
	xp_needed=3**person.level #Xp needed to level up increases exponentially
	if person.XP+1 > xp_needed:
		print(person.name," has leveled up")
		person.level_up()
		print (person.name, "  is now level ", person.level)

def birth(parent_1_first_name,parent_1_surname,parent_2_first_name,parent_2_surname): #Creates new character.
	global all_people
	global rooms
	name=input("Choose a first name for the new child: ")
	if len(name.split())==1: #Player can only input one word
		if name not in used_names:
			name=name[0].upper()+name[1:len(name)] #Capitalizes first letter
			all_people.append(Human(name,day_count,parent_1,parent_2,get_gender()))
			#Following lines let parent's know about their children and their partners.
			parent_1_index=get_person_index(parent_1_first_name,parent_1_surname)
			parent_2_index=get_person_index(parent_2_first_name,parent_2_surname)
			all_people[parent_1_index].children.append(str(name))
			all_people[parent_2_index].children.append(str(name))
			all_people(parent_1_index).partner=str(parent_2)
			all_people(parent_2_index).partner=str(parent_2)
			for r in rooms:
				r.update_assigment()
			if day_count>2: #First few births cost no points
				use_points(50)
			all_people[0].gain_xp(100)
			use_points(25)
			used_names.append(name)
			load_time(5,(name," is being born!"))
		else:
			print("Someone already has that name.")
			birth(parent_1_first_name,parent_1_surname,parent_2_first_name,parent_2_surname)
	else:
		print("You have to input a single word!")
		birth(parent_1_first_name,parent_1_surname,parent_2_first_name,parent_2_surname)
def first_four(): #Runs once at beginning of game. Creates 4 new people. Costs no Action Points!
	global all_people
	global used_names
	global rooms
	names=["Thompson","Elenor","Codsworth","Sharmak","Luthor","Marhsall","Cole","Diven","Davenport","John","Max","Lex","Leth","Exavor"] #Random surnames for inital 5 inhabitants. All children will inherit their surnames from their parents.	if day_count<2: #Initial 5 inhabitants need to be birthed
	for person in all_people:
		used_names.append(str(person.name))
	while len(all_people)<6:
		num_1=randint(0,len(names)-1)
		num_2=randint(0,len(names)-1)
		num_3=randint(0,len(names)-1)
		if num_1==num_2 or num_1==num_3 or num_2==num_3:
			continue
		all_people.append(Human(names[num_1],day_count,names[num_2],names[num_3],get_gender()))
		used_names.append(names[num_1])
		used_names.append(names[num_2])
def create_player(): #Only ran at start of game. First inhabitant of vault should be the player.
	global all_people
	name=input("Choose a first name for yourself: ")
	name=name[0].upper()+name[1:len(name)]
	if len(name.split())==1:
		parent_1=input("What is the surname of your father?")
		if len(parent_1.split())==1:
			parent_1=parent_1[0].upper()+parent_1[1:len(parent_1)]
			parent_2=input("What is the surname of your mother?")
			if len(parent_2.split())==1:
				parent_2=parent_2[0].upper()+parent_2[2:len(parent_2)]
				all_people.append(Human(name,day_count,parent_1,parent_2,get_player_gender()))
			else:
				print("Only single word inputs are accepted.")
				create_player()
		else:
			print("Only single word inputs are accepted.")
			create_player()
	else:
		print("Only single word inputs are accepted.")
		create_player()
def update_all_assignment():
	global rooms
	for r in rooms:
		current_count=len(r.assigned) #Count's how many digits exist
		print("This many digits exist",current_count)
		required_count=len(all_people) #Count's how many digits should exists
		print("How many are needed",required_count)
		if current_count<required_count:
			difference=required_count-current_count
			lst=[]
			for letter in r.assigned:
				lst.append(letter)
			for x in range(difference):
				lst.append('0')
			final=''
			for letter in lst:
				final=final+letter
			print("We're adding this to the assigned",final)
			r.assigned=r.assigned+final
			print("This is what happened", r.assigned)

 
#Inventory managment system!

def rand_item(target_inventory):
	#Following lines randomly choose an item, based on rarity
	num=randint(1,1024) 
	lst=[2**a for a in range(0,11)]
	count=0
	for chance in lst:
		if num<chance:
			break
		count+=1
	rar=10-count #Determines the rarity of an item. 50% chance it's a level 10, 25% chance it's a level 9, 12.5% chance it's a level 8 and so on.
	possible_items=[] #Stores each item if the rarity level matches what was randomly picked.
	for x in all_items:
		if Item(x).rarity==rar:
			possible_items.append(x)
	if len(possible_items)>0:
		number=randint(0,len(possible_items)-1)
		actual_item=possible_items[number]
		#Following lines actually store the item in memory
		if target_inventory=="player":
			add_to_inven(actual_item,1,'inventory')
		elif target_inventory=="trader":
			add_to_inven(actual_item,1,'trader')
		else:
			print("Bug with random item system. Please contact dev!")
def find_rand_item(inven,times): #Finds x items randomly and adds it to an inventory.
	for x in range(0,times+1):
		rand_item(inven)  # passes iven to rand_item function
"""
def remove_from_inventory(it,target_inventory):
	global inventory
	if target_inventory=="player":
		for x in inventory:
			if x==it:	
				inventory.remove(it)
	elif target_inventory=="trader":
		trader_inventory.remove(it)
	break
"""		
		
def add_to_inven(x,number,inven): # Adds (x) (number) times to (inven) inventory. E.g. wood,5,player
	global trader_inventory
	global inventory
	x=str(x)
	inven=str(inven)
	if x not in all_items:
		print("Invalid item. Major bug with inventory adding system. Please contact dev") #Should never happen, since all checks should be done before this function is called.
	else:
		if inven=="player":
			for y in range(number):
				inventory.append(x)
		elif inven=="trader":
			for y in range(number):
				trader_inventory.append(x)

def lose_items(inven,number): #Randomly deletes multiple items from the target_inventory
	global inventory
	global trader_inventory
	if inven=="trader": #Runs daily. Simulates trader selling some items to NPCs.
		for x in range(number):
			rand_number=randint(0,len(trader_inventory)-1)
			trader_inventory.remove(trader_inventory[rand_number])
	elif inven=="player": #Only runs when shelter has been raided by a hostile force.
		print("The raid made off with these items!")
		for x in range(number):
			rand_number=randint(0,len(inventory)-1)
			e=iventory[rand_number]
			print(inventory[e])
			inventory.remove(inventory[e])
	else:
		print("Major bug in item losing system. Please contact dev!")
		
def scrap(it):
	global inventory
	if it not in all_items:
		print("Bug with item scrapping system. Invalid argument passes to function. Please contact dev.")
	else:
		for item in inventory:
			if item==it:
				Item(it).scrap()
				load_time(300,("Scrapping "+str(it)))
				all_people[0].gain_xp((Item(it).rarity)*10)
				break
	use_points(2)



#Raiding system.
def raid():
	global all_people
	update_defense() 
	raiders=["Super Mutant","Raider","Synth","Feral Ghoul"]
	raider=raiders[randint(len(raiders))] #Randomly chooses a raider party.
	attack_power=randint(1,day_count//10)
	load_time(10,("There was a ",raider," raid on your shelter!"))	 
	if defense>attack_power:
		print("But your defenses were strong enough to send them packing!")
	else:
		loss=attack_power-defense
		lose_items("player",loss)
		if loss>10:
			death_chance=loss//10
			dice=randint(2,25)
			if death_chance<dice:
				#Death
				possible_deaths=all_people[1,len(all_people)-1] #The player can't die in a raid!
				death_number=randint(len(possible_deaths))
				print(possible_deaths[death_number]," has been killed in a raid")
				possible_deaths[death_number].die()
	for person in all_people:
		person.gain_xp(attack_power*10)
	use_points(30)
def update_defense(): #Updates the defense rating of the shelter, according to the presence of defensive items.
	global defense
	player=all_people[0]
	defense=0
	turret_count=count_item("turret","player")
	defense+=10*turret_count
	gun_count=count_item("gun","player")
	defense+=gun_count	
	#Add cases for more items that increase defense	
	strength_sum=0
	for person in all_people:
		strength_sum+=person.strength
	defense+=strength_sum
	if player.tactician>0:
		defense=defense*(1+(player.tactician*0.05))
	if player.inspiration>0:
		defense=defense*(1+(player.inspiration*0.03))
	
	
	



#Happiness System.
def avg_hunger(): #Calculates average hunger level.
	total=0
	for x in all_people:
		total+=x.hunger
	avg=total/len(all_people)
	return avg
	
def avg_thirst(): #Calculates average thirst level
	total=0
	for x in all_people:
		total+=x.thirst
	avg=total/len(all_people)
	return avg

def feed(person,amount): #Reduces the hunger level of a person. 
#This needs to reduce the thirst level aswell.
	global all_people
	all_people(person).hunger-=amount
	if all_people(person).hunger<0:
		all_people(person).hunger=0
def drink(person,amount):
	global all_people
	all_people(person).thirst-=amount
	if all_people(person).hunger<0:
		all_people(person).thirst=0
def auto_feed_all():
	global all_people
	food_count=count_item("food","player")
	water_count=count_item("water","player")
	while food_count>0 and avg_hunger()>0:
		for person in all_people:
			feed(person,1)
			food_count-=1
	while water_count>0 and avg_thirst>0:
		for person in all_people:
			drink(person,1)
			water_count-=1
def happiness_loss(): #Depending on hunger or thirst level, reduces general happiness level.
	global happiness
	loss=0
	for y in range(30,101,10):
		if avg_hunger()<y:
			loss+=y-30
			break
	for y in range(30,101,10):
		if avg_thirst()<y:
			loss+=y-30 
			break
	if loss>0:
		happiness-=loss
		print("Due to your inhabitants being hungry and/or thirsty the shelter's overall happiness has dropped to ",happiness)


#Action Point usage system.
#This system is very important and needs to be developed.
#Should deduct from AP. If Ap gets below 0, stores the difference in (overuse). The next day's Action points should be less then.
#For example, if player has 10 action points left, and perfrom an action that costs 20, a day will pass but instead of 50, they'll have 40 action points
def use_points(point):
	global AP
	global overuse
	global overuse_amount
	if point>50:
		print("Bug with point usage system. It's trying to use 50, please note this and contact dev.")
	else:
		usage=AP-point
		overuse=0
		if usage<0: #If overuse occurs. i.e. if overuse is negative
			overuse_amount=0-usage
			overuse=1
		else: #If normal usage occurs. 
			AP=AP-usage
			

	

#Trading system.	
def trade(): #Trading system. Uses no Action Points
	load_time(100,"Initializing trading system.")
	global inventory
	global trader_inventory
	global caps
	global trader_caps
	barter=all_people[0].barter
	stop_trade=0
	while stop_trade==0: #"" lets trading , "break" stops trading
		
		print("Here are the traders' items: ")
		see_inventory("trader") 
		print("The trader has ", trader_caps, " caps.")

		print("Here are your items: ")
		see_inventory("player")
		print("You have ", caps, " caps.")
		
		print("For instance, input (buy 5 food) if you want to buy 5 units of food. Or input (end) to stop trading.")
		a=input("What do you want to do?.")
		
		#Following lines are checks.
		let_trade=0
		if len(a.split())!=3:
			#Allow player to input (buy wood) instead of (buy 1 wood) everytime they only want one of an item.
			if len(a.split())==2: #a is in the form (buy x) or (sell x)
				if a.split()[1] in all_items:
					if a.split()[0]=="buy" or a.split()[0]=="sell":
						a="%s %s %s"%(a.split()[0],1,a.split()[1])
						let_trade=1
					else:
						print("Invalid input. You can (buy) or (sell)")
				else:
					print("This item doesn't exist")	
			elif a.split()[0]=='end' or a.split()[0]=='stop':
				stop_trade=1
			else:
				print("You have to input 3 words. Buy/sell,amount,item")
		elif len(a.split())==3:
			let_trade=1
		if let_trade==1:#Messy conditional routine coming up.
			if a.split()[2] in all_items:
				check=1
				try:
					a.split()[1]=int(a.split()[1])
				except ValueError:
					print("You have to input a number as the second word")
					check=0
				if check==1:
					cost=Item(a.split()[2]).value #Fetches cost of item by tempoarily creating it's object and retreiving it's value attribute
					print("Cost of one item",cost)
					total_cost=cost*int(a.split()[1]) #Sums up the money that is exchanging hands
					print("Cost of all item",total_cost)
					a.split()[0]==a.split()[0].lower()
					if a.split()[0]=="buy":
						#Adjusts the prices, depending on bartering level.
						for x in range(0,4):
							total_cost=int(total_cost*(1.2-(x*0.05)))
						if total_cost>caps:
							print("You can't afford that!")
						else:
							count=count_item(a.split()[2],"trader")
							if int(a.split()[1])>count:
								if count==0:
									print("The trader doesn't have any ",a.split()[2])
								else:
									print("The trader doesn't have ",a.split()[1]," of ",a.split()[2])
							else:
								for x in range(int(a.split()[1])):
									trader_inventory.remove(str(a.split()[2]))
									inventory.append(a.split()[2])
								caps-=total_cost
								trader_caps+=total_cost	
					elif a.split()[0]=="sell":
						#Adjusts the prices, depending on bartering level.
						for x in range(0,4):
							total_cost=int(total_cost*(0.8+(x*0.05)))
						if total_cost>trader_caps:
							print("The trader can't afford that!")
						else:
							count=count_item(a.split()[2],"player")
							if int(a.split()[1])>count:
								if count==0:
									print("You don't have any ",a.split()[2])
								else:
									print("You don't have ",int(a.split()[1])," of ",a.split()[2])
							else:
								for x in range(int(a.split()[1])):
									inventory.remove(str(a.split()[2]))
									trader_inventory.append(a.split()[2])
								trader_caps-=total_cost
								caps+=total_cost
					else:
						print("Invalid Input. (buy) and (sell) are accepted")
				else:
					print("Only numbers are accepted")					
			else:
				print("Sorry. ",a.split()[2]," doesn't exist!")	
	load_time(100,"Ending trade")
					
#Production system
def produce_all(): #Causes production of all rooms.
	global rooms
	for r in rooms:
		if r.can_produce==1:
			r.update_production() 
			if r.name=="kitchen":
				for x in range(r.production//10):
					add_to_inven("food")
			elif r.name=="generator":
				for x in range(r.production//10):
					add_to_inven("watt")
			elif r.name=="water works":
				for x in range(r.production//10):
					add_to_inven("water")
			#Add more cases for each production capable room
			
				

	
#Choice system!
def choice():
	global auto_feed
	global all_people
	global rooms
	a=input("Choose what to do:")
	if len(a)>0:
		if a.split()[0]=="build": #Allows player to build new rooms. Checks if player has components to build room.
			if len(a.split())!=2:
				print("You have to input 2 words to build a room.")
			elif not check_room(a.split()[1]):
				print("This room doesn't exist.")
			elif check_built_room(a.split()[1]):
				print("You've already built this room.")
			else:
				room=Room(a.split()[1])
				checked=[] #Stores components already checked. Useful. If there's 5 pieces of wood in the components list, the loop is only run once, instead of 5 times
				for component in room.components:
					if component not in checked:
						number_available=count_item(component,"player")
						number_needed=room.count_component(component)
						if number_needed>number_available: 
							print("You don't have enough", component,"to build",a.split()[1])
							can_craft=0
						checked.append(component)
						
				if can_craft==1:
					print("You have crafted a", a.split()[1])
					craft(a.split()[1])
				
		elif a.split()[0]=="craft":
			#Checks to see if crafting possible.
			if a.split()[1] not in all_items:
				print("Invalid item. Try again.")
			else:
				can_craft=1
				actual_item = Item(a.split()[1]) #Creates an instance of the item, so it's attributes can be fetched.
				if len(actual_item.components)==0:
					print("This is a basic item and so cannot be crafted.")
				else:
					checked=[]
					for component in actual_item.components:
						if component not in checked:
							number_available=count_item(component,"player")
							number_needed=actual_item.count_component(component)
							if number_needed>number_available: 
								print("You don't have enough", component,"to craft",a.split()[1])
								can_craft=0
							checked.append(component)
					if can_craft==1:
						print("You have crafted a", a.split()[1])
						craft(a.split()[1])
						
		elif a.split()[0]=="scrap":
			if len(a.split())==2: #Only scrap item once.
				if a.split()[1] not in all_items:
					print("Invalid item. Please try again.")
				else:
					count=count_item(str(a.split()[1]),"player")
					if count>0:
						scrap(a.split()[1])
					else:
						print("You don't have that item.")
			elif len(a.split())==3: #Scrap multiple times
				if a.split()[1] in range(1,100):
					if a.split()[2] in all_items:
						count=count_item(str(a.split()[1]),"player")
						if count>=a.split()[1]:
							for x in range(a.split()[1]):
								scrap(a.split()[2])
						else:
							print("You don't have enough of these items to scrap that many times.")
					else:
						print("This item doesn't exist.")
				else:
					print("Invalid input. You can scrap an item up to 99 times (If you have that many).")
			else:
				print("Invalid Input. Either enter (scrap wood) or (scrap 5 wood)")
						
		elif a.split()[0]=="rush":#Speeds up room tempoarily. Needs a lot of work. room.Rush() method incomplete.
			if a.split()[1] not in all_rooms:
				print("This room doesn't exist. Input (see rooms) to view all your rooms.")
			elif rooms(a.split()[1]).can_rush==0:
				print("This room cannot be rushed")
			else:
				room_index=get_room_index(a.split()[1])
				rooms[room_index].rush()
			
		elif a.split()[0]=="see":
			if a.split()[1]=="people":
				see_people()
			elif (a.split()[1])=="items":
				see_inventory("player")
			elif a.split()[1]=="rooms":
				see_rooms()
			elif a.split()[1]=="day":
				print("Today is day",day_count)
			elif a.split()[1]=="resources":
				see_resources()
			else:
				print("Incorrect input. To see people, input (see people). To view your inventory, input (see inventory) ")
				
		elif a.split()[0]=="coitus": #Allows player to create new inhabitants
			people_names=[a.name for a in all_people] #Used to check input
			if len(a.split())!=5:
				print("You need to input 2 mature people of opposite genders.")
			elif not check_person(a.split()[1],a.split()[2]):
				print("No such",a.split()[1]," exists!")
			elif not check_person(a.split()[3],a.split()[4]):
				print("No such",a.split()[2]," exists!")
			elif len(all_people)==living_capacity():
				print("You've reached the vault's maximum capacity. Upgrade your living room to hold more people")
			else:
				person_1_index=get_person_index(a.split()[1],a.split()[2])
				person_2_index=get_person_index(a.split()[3],a.split()[4])
				person_1=all_people[person_1_index]
				person_2=all_people[person_2_index]
				if (person_1.partner=="" and person_2.partner=="") or person_1.partner==person_2.name:			
					if person_1.age <18:
						print(a.split()[1]," isn't old enough to copulate.")					
					elif person_2.age <18:
						print(a.split()[2]," isn't old enough to copulate.")
					elif person_1.surname==person_2.surname:
						print("Sorry. Incest isn't allowed. At least be ethical!")
					elif person_1.gender==person_2.gender:
						print("The people need to be different genders! COME ON MAN CAN U EVEN BIOLOGY!")
					else:
						birth(person_1.name,person_1.surname,person_2.name,person_2.surname) #Pass these love birds to the birthing system
				else:	
					print("Infedility shall not be allowed!!!")
					print(person_1.name,"  is married to ",person_1.partner)
					print(person_2.name,"  is married to ",person_2.partner)
				
		elif a.split()[0]=="feed": #Checks if player has enough food to feed person and then calls feed(person) function.
			food_count=count_item("food") #Counts how much food is available for feeding
			if avg_hunger()<2:
				print("You're people are working on full bellies boss!")
			elif len(a.split())==2: #If player wants to feed only one person
				if a.split()[1] not in all_people: #Checks if chosen Human exists
					print("This person doesn't exist.")
				else:	
					hunger=all_people(a.split()[1].hunger) #Fetches hunger level of selected Human
					amount=input("Feed ",a.split()[1],"  by how much?")
					if amount<hunger:
						print("You don't have enough food to feed ",a.split()[1])
					else:
						feed(a.split()[1],amount)
			else: 
				print("Invalid input! Can only feed one person like this. Use the auto_feed system to feed everyone.")
				
		elif a.split()[0]=="trade":
			if not check_built_room('trader'):
				print("You haven't built a trader room yet!")
			elif '1' not in str(rooms[get_room_index('trader')].assigned):
				print("No one has been assigned to this room! You can't trade untill then.")
			else:
				trade()
				
		elif a.split()[0]=="assign":
			if len(a.split())!=5:
				print("You have to input 4 words. E.g. assign Thomas Marc to living")
			elif not check_person(a.split()[1],a.split()[2]):
				print("This ",a.split()[1]," doesn't exist.")
			elif not check_room(a.split()[4]):
				print("This room doesn't exist.")
			elif not check_built_room(a.split()[4]):
				print("You haven't built this room yet")
			elif rooms[get_room_index(a.split()[4])].assigned_limit==rooms[get_room_index(a.split()[4])].count_assigned():
				print("This room is full.")
				print("You can assign someone in the room to another room to create space.")
			else:
				person_index=get_person_index(a.split()[1],a.split()[2])
				all_people[person_index].assign_to_room(a.split()[4])
			
		elif a.split()[0]=="upgrade":
			if not check_room(a.split()[1]) or not check_built_room(a.split()[1]):
				print("This room doesn't exist. Try again.")
			elif a.split()[1]=="trader":
				print("This room cannot be upgraded")
			else:
				r=rooms[get_room_index(a.split()[1])] #Tempoarily fetches room so it's attributes can be used
				items_needed=r.components
				for x in range(r.level-1): #The higher the level, the more components needed to upgrade
					for component in items_needed:
						items_needed.append(component)	
				can_up=1 #Can the room be upgraded or not?
				for ite in all_items: #For each item
					needed=0 #Counts how many are needed
					for comp in items_needed: 
						if ite==comp:
							needed+=1
					available=count_item(ite,"player") #Counts number of component available to the player
					if available<needed:#Not enough
						can_up=0
						print("You don't have enough",ite, "to upgrade your ", r.name)
						break
				if can_up==1:
					for component in items_needed:
						inventory.remove(component)
					r.upgrade()
					print(r.name,"has been upgraded and is now level",r.level)
					
		elif a.split()[0]=="disable":
			if a.split()[1]=="auto":
				auto_feed=0
				print("Warning. You have disabled the auto_feed feature. Be careful, your people may starve!")
			else:
				print("Invalid input. You can disable the (auto_feed) system.")
				
		elif a.split()[0]=="enable":
			if a.split()[1]=="auto":
				auto_feed=1
				print("Auto-feed system is working optimally.")
			else:
				print("Invalid Input. You can enable the (auto_feed) system.")
				
		elif a.split()[0]=="scavenge":
			if a.split()[1] not in all_people:
				print("This person doesn't exist.")
			elif all_people(a.split()[1]).scavenging==1:
				print("This person is already out scavenging.")
			else:
				cho=input("Would you like to scavenge for a certain number of days or until their health gets low?(D/H)")
				cho=cho[0].lower()
				if cho=="d":
					scavenge(a.split()[1],"days")
				elif cho=="h":
					scavenge(a.split()[1],"")
				else:
					print("Let's just assume you wanted them to go out until their health gets low.")
					scavenge(a.split()[1],"")
					
		elif a.split()[0]=="heal":
			if a.split()[1]=="all":
				heal_all()
			else:
				if a.split()[1] not in all_people:
					print("That person doesn't exist.")
				else:
					stim_count=count_item("stimpack","player")
					if stim_count>0:
						all_people(a.split()[1]).heal(heal_amount)
		elif a.split()[0]=="skip":
			global skip
			skip=1
		elif a.split()[0]=="end":
			global player_quit
			confirm=input("Are you sure? All unsaved data will be lost!")
			confirm=confirm[0].lower()
			if confirm=="y":
				player_quit=1	
		else:
			print("Invalid Input. Try again.")
	else:
		print("You have to choose something!")
		

	

#Game system.
def game():
	global AP
	global day_count
	global end
	global postition
	global inventory
	global rooms
	global caps
	global trader_inventory
	global trader_caps
	global defense
	global overuse
	global happiness
	global overuse
	global auto_feed
	global overuse_amount
	global all_items
	global all_people
	global all_rooms
	global postition
	global used_names
	global player_quit
	global skip
	load_time(300,"Initializing game.")
	
	day_count=1
	end=0 #Can lose postition or die.  This is used for a while loop.
	postition="secure" #Only changed to "lost" when happiness drops below 5.
	player_quit=0 #Allows player to quit the game.
	inventory=[] #All items that belong to the player. Just names
	rooms=[Room('living'),Room('kitchen')] #Rooms that player has built. Objects!
	all_people=[] #All the people alive in the shelter. Objects!	
	used_names=[] #Names that have been used in the game. Ensures no two people have the same name.
	all_items=["wood","steel","turret","food","water","wire","silicon","electronic chip"] #Stores every possible item in the inventory. Just names.
	all_rooms=["living","bath","generator","kitchen","trader","storage"] #Stores every possible room in the game. Just names.
	all_attributes=["strength","perception","endurance","charisma","intelligence","luck","medic","science","tactitian","cook","inspiration","scrapper","barter","electrician"]
	
	caps=100
	trader_caps=400
	happiness=100
	trader_inventory=[]
	find_rand_item("trader",20) #Initializes trader inventory with 20 random items.
	defense=0 
	overuse=0#Keeps track of whether or not player has used too many action points.
	auto_feed=1 #Can be set to 0 by player to conserve food.  Recomended to only do so during emergencies.
	overuse=0
	
	print("Welcome to the text-based fallout shelter game!")
	print("Welcome, great Overseer!")
	print("It is your great duty to increase the population of your vault and keep your inhabitants happy.")
	create_player()
	load_time(100,"Creating player.")
	all_people[0].age=20
	first_four()
	load_time(200,"Populating Vault with 5 random inhabitants")
	update_all_assignment()
		
	#Put Instructions for player here
	print("Commands: ")
	print("see people: View all inhabitants")
	print("see items: View all items")
	print("build x: Consruct a room")
	print("craft x: Craft an item")
	print("scrap x: Destroy an item and add it's components to your inventory")
	print("enable auto_feed: Enable the automatic inhabitant feeding system")
	print("disable auto_feed: Disable the automatic inhabitant feeding system")
	print("trade: Begin trading interaction")
	print("coitus x y: Send daddy and mommy to the love-house")
	print("scavenge x: Send x on a scavenging mission")
	print("")
	print("You have been given 100 caps to start your journey.")
	AP=50
	build('trader')
	craft('turret')
	update_all_assignment()
	while end==0 and postition=="secure" and player_quit==0: #Loops the day while player is alive,is still the overseer and doesn't decide to quit.
		print("Here is the trader's assigned variable",rooms[get_room_index('trader')].assigned)
		AP=50
		if overuse==1:
			AP=50-overuse_amount
		print("Today is day ",day_count)
		load_time(300,"A new day dawns.")
		
		
		for person in all_people: #Performs daily checks for all people.
			if person.name != all_people[0].name: #Routines specific to NPCs.
				#Hunger Games.
				person.hunger+=10
				if person.hunger>99:
					print(person.name,person.surname," has died of hunger")
					person.die()
				elif person.hunger>80:
					print("Warning!",person.name,person.surname," is starving and may die soon.")
				elif person.hunger>50:
					print(person.name,person.surname," is hungry.")
				#Thirsty games.
				person.thirst+=10
				if person.thirst>99:
					print(person.name,person.surname," has died of thirst")
					person.die()
				elif person.hunger>80:
					print("Warning!",person.name,person.surname," is extremely thirsty and may die soon.")
				elif person.hunger>50:
					print(person.name,person.surname," is thirsty.")
				#Scavenging games
				if person.scavenging == 1:
					if person.daysToScavengeFor == person.daysScavenging:
						# Now that they've finished scavenging, set everything to 0
						person.Scavenging = 0
						person.daysToScavengeFor = 0
						person.daysScavenging = 0
					else:
						person.daysScavenging += 1
						#Randomly finds an item
						rand_item("player")
						health_loss=randint(0,50)
						person.take_damage(health_loss)
						person.gain_xp(randint(10,200))
					if person.health<20:
						person.scavenging=0
						person.daysToScavengeFor = 0
						person.daysScavenging = 0
				#Experience games
				if person.assigned_room!="":
					r=rooms(assigned_room) # Can refer to room which character had been assigned to.
					person.gain_xp(r.production//10)
			#Level Up games
			check_xp(person.name,person.surname) #Checks if person has enough xp to level up.	
		
		if auto_feed==1:
			auto_feed_all()		
		
		for r in rooms: #Performs daily room checks.
			if r.can_produce==1:
				if r.rushed==1:
					r.production-=50
					r.rushed=0
		produce_all() #Causes all rooms that can produce, to produce.
		#Also updates production of all rooms.
		
		#Trader inventory updates with new items and loses some items.
		number=randint(0,(len(trader_inventory)//5)) #Loses a random number of items
		lose_items("trader",number) 
		number=randint(0,len(trader_inventory)//5) #Finds another random number.
		find_rand_item("trader",number) #Finds random number of items.
		
		#A raid should happen once every 5 days.
		raid_chance=randint(1,5)
		if day_count<11:
			raid_chance=1 #No raids should happen in the early days.
		if raid_chance>4:
			raid()
			
		if happiness<5:
			postition="lost"
		elif happiness<20:
			print("Warning. Your people are unhappy. You could lose your position if you don't improve the situation soon.")
		skip=0	
		while AP>0 and overuse==0 and player_quit==0: #Loops player actions.
			choice()
			if skip==1:
				break
				
		print("Due to your shelter's happiness level you have gained ", happiness//10, " experience")
		all_people[0].gain_xp(happiness//10)
		happiness_loss()
		day_count+=1
			
	else: #Once game ends.
		if end==1:
			print("Too bad. You died.")
		elif postition=="lost":
			print("Too bad. You lost your postition because of your poor leadership skills.")
		again=input("Want to play again?")
		again=again[0].lower()
		if again=="y":
			game()
		else:
			print("Okay. Thanks for playing!!!")
game()
