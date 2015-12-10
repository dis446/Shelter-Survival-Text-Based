from random import randint
class human(object):
	def __init__(self,name,day_of_birth,parent_1,parent_2,gender):
		if all_people <6 or day_count<5: #First 5 people will be 21 years old, so they can mate.
			self.age=18
		else:
			self.age=0
		self.hunger=0
		self.name = name
		self.parent_1=parent_1
		self.parent_2=parent_2
		self.gender=gender[0].lower()
		self.strength=1
		self.perception=1
		self.endurance=1
		self.charisma=1
		self.intelligence=1
		self.luck=1
		self.can_mate=0
		self.children=[]
	def mature(self):
		self.age+=1
		print(self.name," has matured and is now ",self.age," years old!")
	def rebirth(self):
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
	def can_mate_check(self): #Checks if person can have coitus and have children. Perfomed twice when player inputs coitus.
		if self.age <18:
			self.can_mate=0
		elif len(self.children)>5:
			self.can_mate=0
		elif len(self.children)==0:
			self.can_mate=1
		for child in self.children:
			if child.age<1:
				self.can_mate=0
	def die(self):
		global end
		all_people.remove(self)
		print(self," has died")
		if all_people[0]==self.name:
			end=1
		
class room(object):
	def __init__(self,name,benefits,risk,inhabitants):
		self.name=name
		self.benefits=benefits
		self.risk=risk
		self.inhabitants=inhabitants
		self.production=100
	def rush(self): #Needs a lot of work!!! Like nothings done. Like nothing
		self.production+=10
	def produce(self): #What is this???
		inventory.append(self.benefits*production)
	def destroy(self):
		global rooms
		rooms.remove(self)
	
class item(object):
	def __init__(self,name,number,value,weight,components):
    	self.name=name
    	self.number=number
    	self.value=value #Can be sold to merchant's for caps.
    	self.weight=weight
    	self.components=components
    	self.scrapped=0
    def scrap(self):
		print(self.name," has been scrapped and these")
		for item in self.components:
			inventory.append(item)
			print(item)
		print("have been added to your inventory")
		self.destroy()
		self.scrapped=1 Differentiate between whether item has been scrapped or just destroyed
	def destroy(self):
		global inventory
		inventory.remove(self)
		if self.scrapped!=1:
			print(self.name," has been destroyed!")

def input_int(x): #Whenever has to input an integer, this should be used.
	x=input("Input an integer.")
	try:
		int(x)
	else ValueError:
		print("Invalid. Only integer numbers are accepted!")
		x=input("Try again. Input:")
		check_int(x)
	return x
		
	
def get_player_gender():#Asks player what gender they are
	gender=input("Please choose a gender.(M/F)")
	gender=gender[0].lower()
	if gender!="m" or "f":
		print("Invalid gender choice!")
		get_gender
	return gender
	
def get_gender(): #For NPCs
	gender=randint(0,1):
	if gender==0:
		gender="m"
	else:
		gender="f"
	return gender
	
def create_player():#Only ran at start of game. First inhabitant of vault should be the player.
	global all_people
	name=input("Choose a first name for yourself: ")
	surname=input("Choose a surname for yourself: ")
	parent_1=input("What is the surname of your father?")
	parent_2=input("What is the surname of your mother?")
	all_people.append(human(name,day_count,parent_1,parent_2,get_player_gender)


	
	
def build(room): #Actually builds the room once checks are done.
	global rooms
	global AP
	room=str(room)
	if room=="living":
		str(room)=room(str(str(room)+"_room_count"),[],0,[])
		living_room_count+=1
		str(str(room)+"_room_count)")+=1
	elif room=="bath":
		str(room)=room(str(str(room)+"_room_count"),[],10,[])
	elif room=="oil":
		str(room)=room(str(str(room)+"_room_count"),[],40,[])
	elif room=="thermal":
		str(room)=room(str(str(room)+"_room_count"),[],30,[])
	elif room=="kitchen":
		str(room)=room(str(str(room)+"_room_count"),[],20,[])
	rooms.append(str(str(room)+"_room_count"))
	AP-=20
	
def craft(item):#Actually crafts the item once checks are done
	global inventory
	global AP
	#Need to study code
	AP-=10

def birth(parent_1,parent_2): #Creates new NPC.
	global AP
	global all_people
	name=input("Choose a first name for the new child: ")
	if len(name)!=1:
		print("You have to input a single word!)
		birth(parent_1,parent_2)
	all_people.append(human(name,name,day_count,parent_1,parent_2,get_gender)
	AP-=50

def feed(person,food): #Reduces the hunger level of a person
	global all_people
	all_people(person.hunger)-=food
	if all_people(person.hunger)<0:
		print("Major error. Please contact developer!")
	
def choice():
	a=input("Choose what to do:")
	if a.split()[0]=="build":#Allows player to build new rooms. Checks if player can build
		if a.split()[1] not in all_rooms:
			print("Invalid room. Try again.")
			choice()
		for component in all_rooms[a.split()[1].components]:
			component_count=count_item(component)
			for item in inventory:
				if item==component:
					item_count=count_item(item)
				if item_count<component_count:
					print("You don't habe the required components to craft this item")
					choice()
		build(a.split[1])
	elif a.split()[0]=="craft":#Crafting system. The-9880 assigned to this. Checks to see if player can craft. Maybe want to allow player to craft one item multiple times.
		if a.split()[1] not in all_items:
			print("Invalid item. Try again.")
			choice()
		craft(a.split()[1])
	elif a.split()[0]=="rush":#Speeds up room tempoarily. Needs a lot of work
		if a.split()[1] not in all_rooms:
			print("Invalid room. Try again.")
			choice()
		if a.split()[1] not in rooms:
			print("Room doesn't exist yet. Perhaps you can build it!")
			choice()
		a.split[1].rush()
	elif a.split()[0]=="coitus": #Allows player to create new inhabitants
		if len(a)!=3:
			print("You need to input 2 mature people of opposite genders.")
			choice()
		if a.split()[1] not in all_people:
			print("No such",a.split()[1]," exists!")
			choice()
		if a.split()[2] not in all_people:
			print("No such",a.split()[2]," exists!")
			choice()
		if a.split()[1].age <18:
			print(a.split()[1]," isn't old enough to copulate.")
			choice()
		if a.split()[2].age <18:
			print(a.split()[2]," isn't old enough to copulate.")
			choice()
		if a.split()[1].gender==a.split()[2].gender:
			print("The people need to be different genders! COME ON MAN CAN U EVEN BIOLOGY!")
			choice()
		birth(a.split()[1],a.split()[2])
		
		
		
	elif a.split()[0]=="feed": #Checks if player has enough food to feed person and then calls feed(person) function.
		food_count=count_item("food") #Counts how much food is available for feeding
		print("You have ",food_count," items of food.")
		avg_hunger=avg_hunger() #Fetches average hunger level. Used if player tries to feed everyone.
		if len(a.split())==2: #If player wants to feed only one person
			if a.split()[1] not in all_people: #Checks if chosen human exists
				print("This person doesn't exist.")
				choice()
			hunger=all_people(a.split()[1].hunger) #Fetches hunger level of selected human
			amount=input("Feed ",a.split()[1],"  by how much?")
			if amount<hunger:
				print("You don't have enough food to feed ",a.split()[1])
			else:
				feed(a.split(),amount)
		else:
			if a.split()[1]=="all":
				amount=input("By how much each?(You have ",food_count," food to use)")
				if amount<avg_hunger:
					print("You can't feed all those people")
					choice
				for person in all_people:
					person.feed()
					
	elif a.split()[0]=="trade":
		if "trader" not in built_room_types:
			print("You haven't built a trader room yet!")
			choice()
		elif all_rooms.("room".inhabitants)==0:
			print("No one has been assigned to this room! You can't trade untill then.")
			choice()
		
	else:
		print("Invalid Input. Try again.")
		choice()


def see_people(): #Allow player to see all the inhabitants so they can plan. Should display name, age, gender and hunger level
	pass
def add_to_inven(x,number):
  x=str(x)
  if x not in all_items:
    print("Invalid item. Major bug. Please contact dev")
  if x=="wood": 
    for x in range(0,number):
      inventory.append(item("wood",number,10,[])
  elif x=="gun":
    for x in range(0,number):
      inventory.append(item("gun",number,50,["metal","metal","sight"])
  #Add special cases for all in-game items, with their own seperate values, weights and components#


def count_room(room):#Counts total number of a room.
	count=0
	for x in all_rooms:
		if x==room:
			count+=1
	return count

def count_item(item):#Counts total number of an item
	count=0
	for x in all_items:
		if x==item:
			count+=1
	return count
	
def see_inventory():  #Displays all items in inventory in the form (Log*5,Gun*6).
	for item in all_items:
		print(item,"*",count_item(item))
		
		
def avg_hunger(): #Calculates average hunger level.
	total=0
	for x in all_people:
		total+=x.hunger
	avg=total/len(all_people)
	return avg
	
def happiness_loss(x): #Depending on hunger loss, reduces general happiness level.
	global happiness
	for y in range(20,101,10):
		if x<y:
			loss=100-y
			break
	happiness-=loss
	print("Due to your inhabitants being hungry the shelter's overall happiness has dropped to ",happiness)
	
def loop():#Needs reworking
	day_count=1
	end=0 #Can lose postition or die.  This is used for a while loop.
	print("Welcome to my fallout shelter game!")
	print("Welcome, great Overseer!")
	print("It is your great duty to increase the population of your vault and keep your inhabitants happy!")
	player_name=input("Please choose a name.")
	player_parent_1=input("What is the name of your father?")
	player_parent_2=input("What is the name of your mother?")
	player=birth(player_name,player_parent_1,player_parent_2)
	player.age=20
	postition="secure"
	inventory=[] #All items that belong to the player
	print("Commands:/n")
	#Put Instructions for player here
	all_items=[] #Stores every possible item in the inventory
	all_room_types=["living","bath","generator","kitchen","trader"] #Stores every possible room type in the game. Just names.
	built_room_types=[] #Each time player builds a room type that they've never built before, it's appended here. Used to keep track of progress. Used to hold the actual instantces of the class(room)
	rooms=[] #Rooms that player has built.
	all_people=[] #All the people alive in the shelter.
	caps=100
	happiness=100
	while end==0 and position=="secure": #Loops the day
		hibernate=0 # Allows players to store their APs for later.
		for person in all_people: #Increases hunger level of everyone in the vault.
			person.hunger+=10
			if person.hunger>100:
				person.die()
				print(person.name," has died of hunger")
			elif person.hunger>80:
				print("Warning!",person.name," is starving and may die soon.")
			elif person.hunger>50:
				print(person.name," is hungry.")
			
	
		AP=50 #Let's player perform actions.
		print("Today is day ".day_count)
		if happiness<2:
				postition="lost"
		elif happiness<20:
			print("Warning. Your people are unhappy. You could lose your position.")
		hunger=avg_hunger()
		happiness_loss(hunger)
		while AP>0 and hibernate==0: #Loops player actions.
			choice()
	else:
		if end==1:
			print("Too bad. You died.")
		elif postition=="lost":
			print("Too bad. You lost your postition because of your poor leadership skills.")
		again=input("Want to play again?")
		again=again[0].lower()
		if again=="y":
			loop()
		else:
			print("Okay. Thanks for playing!!!")
	
			
