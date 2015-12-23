class human(object):
	def __init__(self,name,age,day_of_birth,parent_1,parent_2,gender,strength,perception,endurance,charisma,intelligence,luck):
		self.name=name
		self.age=0
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
		if self.name=="player":
			self.can_mate=1
	def mature(self):
		self.age+=1
	def rebirth(self):
		self.age=0
		if self.gender=="f":
			print(self," has been reborn and his stats have been reset")
		else:
			print(self," has been reborn and her stats have been reset")
		self.strength=1
		self.perception=1
		self.endurance=1
		self.charisma=1
		self.intelligence=1
		self.luck=1
	def can_mate_check(self):
		if self.age <18:
			self.can_mate=0
		elif len(self.children)>5:
			self.can_mate=0
		if len(self.children)==0:
			self.can_mate=1
		for child in self.children:
			if child.age<1:
				self.can_mate=0
		if self.can_mate==0:
			print("Sorry.",self," cannot mate.")
		else:
			print("Congratulations!", self," can mate.")
		
			
	def die(self):
		self.status="dead"
		print(self," has died")
		
class room(object):
	def __init__(self,number,benefits,risk,inhabitants):
		self.benefits=benefits
		self.risk=risk
		self.inhabitants=inhabitants
		self.number=number
		self.production=100
	def rush(self):
		self.production+=10
	def produce(self):
		inventory.append(self.benefits*production)
	def destroy(self):
		self.status="rekt"#If room is ever mentoined again, this will ensure it can't be used.E.g. If player attempts to rush room, it will say "room has been rekt"
class item(object):
	def __init__(self,value,weight,components):
		self.value=value
		self.weight=weight
		self.components=components
	def scrap(self):
		for item in self.components:
			inventory.append(item)
		self.status="rekt"
		
def birth(name,parent_1,parent_2):
	name=str(name)
	parent_1=str(parent_1)
	p		arent_2=str(parent_2)
	str(name)=human(name,0,parent_1,parent_2)
	
"""
Initilize room count:
living_room_count=1
oil_room_count=1
thermal_room_count=0
bath_room_count=0
kitchen_room_count=1
"""	
def build(room):
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
def craft(item):
	requirements=item.components
	#Need to check if player has all items needed to craft
def choice():
	a=input("Choose what to do:")
	if a.split()[0]=="build":
		if a.split()[1] not in all_rooms:
			print("Invalid room. Try again.")
			choice()
		build(a.split[1])
	elif a.split()[0]=="craft":
		if a.split()[1]  not in all_items:
			print("Invalid item. Try again.")
			choice()
		craft(a.split()[1])
	elif a.split()[0]=="rush":
		if a.split()[1] not in all_rooms:
			print("Invalid room. Try again.")
			choice()
		if a.split()[1] not in rooms:
			print("Room doesn't exist yet. Perhaps you can build it!")
			choice()
		a.split[1].rush()
	elif a.split()[0]=="coitus":
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
		
			
		
	else:
		print("Invalid Input. Try again.")
		choice()
		
def see_inventory():
	for a in all_items:
		count=0
		for item in inventory:
			if a==item:
				count+=1
		print(a,"*",count)
		
	
def loop():#Needs reworking
	day_count=1
	end=0#Can lose postition or die.
	print("Welcome to my fallout shelter game.")
	print("Welcome, great Overseer!")
	print("It is your great duty to increase the population of your vault and keep your inhabitants happy!")
	player_name=input("Please choose a name.")
	player_parent_1=input("What is the name of your father?")
	player_parent_2=input("What is the name of your mother?")
	player=birth(player_name,player_parent_1,player_parent_2)
	player.age=20
	postition="secure"
	inventory=[]
	print("Commands:/n")
	all_items=[]
	all_items=[item.append("_",a) for a,item in range(0,101),all_items] #Python 3.4 fixes the error here if you remove the last parameter
	all_rooms=[]
	all_rooms=[room.append("_",a) for a,room in range(0,101),all_rooms]
	rooms=[]
	all_people=[player]
	while end==0:
		AP=50
		print("Today is day ".day_count)
			
			
		
		
"""
class weapons(item):
	damage = 0
	type = 0
	clip_Size = 0
	
	def fire(self):
		
		
	
	def 
	
	
class item(object):
	def __init__(self,value,weight,components):
		self.value=value
		self.weight=weight
		self.components=components
	def scrap(self):
		for item in self.components:
			inventory.append(item)
		self.status="rekt"


"""