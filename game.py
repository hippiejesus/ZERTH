import random
import sys
import pprint
import subprocess
import platform

pp = pprint.PrettyPrinter(indent = 3)

start = ['----------------',
         '----------------',
         '----------------',
         '----------------',
         '----------------',
         '----------------',
         '----------------']

def clear():
    subprocess.Popen( "cls" if platform.system() == "Windows" else "clear", shell=True)


class character:
    def __init__(self,name,identity,stats,controller):
        self.name = name
        self.identity = identity
        self.stats = stats
        self.brain = controller
        self.location = (0,0)
        self.sublocation = [3,3]
        self.avatar = '@'
        self.inventory = []
        self.equipped = {}
        self.world = None
    def act(self,situation):
        self.brain.act(situation)
    def die(self):
        self.location = (None,None)
    def move_n(self):
        self.sublocation[1] -= 1
    def move_s(self):
        self.sublocation[1] += 1
    def move_w(self):
        self.sublocation[0] -= 1
    def move_e(self):
        self.sublocation[0] += 1
    def wait(self):
        pass
    def status(self):
        global pp
        print()
        print(self.name + ':\n')
        pp.pprint(self.stats)
        print()
    def inv(self):
        global pp
        print()
        print('Inventory: \n')
        pp.pprint(self.inventory)
        print()
    def equip_check(self):
        global pp
        print()
        print('Equipped: \n')
        pp.pprint(self.equipped)
        print()
    def attack_n(self,situation):
        for i in situation.entities:
            if i.sublocation[0] == self.sublocation[0] and i.sublocation[1] == self.sublocation[1] - 1:
                damage = self.brain.calculate_damage()
                self.world.set_enemy(i,self)
                if random.randint(0,i.stats['action']['guile']) > damage:
                    print(i.name+" dodges the blow!")
                else:
                    damage_blocked = i.stats['action']['physicality'] / 5 - damage
                    if damage_blocked >= 0:
                        print(i.name+" shrugs off the blow!")
                    else:
                        self.world.change_health(i,damage_blocked)
                        print(i.name+" catches a blow for "+str(abs(damage_blocked))+" damage!")

    def attack_s(self,situation):
        for i in situation.entities:
            if i.sublocation[0] == self.sublocation[0] and i.sublocation[1] == self.sublocation[1] + 1:
                damage = self.brain.calculate_damage()
                self.world.set_enemy(i,self)
                if random.randint(0,i.stats['action']['guile']) > damage:
                    print(i.name+" dodges the blow!")
                else:
                    damage_blocked = i.stats['action']['physicality'] / 5 - damage
                    if damage_blocked >= 0:
                        print(i.name+" shrugs off the blow!")
                    else:
                        self.world.change_health(i,damage_blocked)
                        print(i.name+" catches a blow for "+str(abs(damage_blocked))+" damage!")
    def attack_e(self,situation):
        for i in situation.entities:
            if i.sublocation[1] == self.sublocation[1] and i.sublocation[0] == self.sublocation[0] + 1:
                damage = self.brain.calculate_damage()
                self.world.set_enemy(i,self)
                if random.randint(0,i.stats['action']['guile']) > damage:
                    print(i.name+" dodges the blow!")
                else:
                    damage_blocked = i.stats['action']['physicality'] / 5 - damage
                    if damage_blocked >= 0:
                        print(i.name+" shrugs off the blow!")
                    else:
                        self.world.change_health(i,damage_blocked)
                        print(i.name+" catches a blow for "+str(abs(damage_blocked))+" damage!")
    def attack_w(self,situation):
        for i in situation.entities:
            if i.sublocation[1] == self.sublocation[1] and i.sublocation[0] == self.sublocation[0] - 1:
                damage = self.brain.calculate_damage()
                self.world.set_enemy(i,self)
                if random.randint(0,i.stats['action']['guile']) > damage:
                    print(i.name+" dodges the blow!")
                else:
                    damage_blocked = i.stats['action']['physicality'] / 5 - damage
                    if damage_blocked >= 0:
                        print(i.name+" shrugs off the blow!")
                    else:
                        self.world.change_health(i,damage_blocked)
                        print(i.name+" catches a blow for "+str(abs(damage_blocked))+" damage!")

class world:
    def __init__(self):
        global start
        self.rooms = {(None,None):room((None,None),None,None),(0,0):room((0,0),None,start)}
        self.characters = {}
        self.items = {}
    def spawn(self,entity):
        if isinstance(entity,character):
            entity.world = self
            self.characters.update({entity.name:entity})
        elif isinstance(entity,item):
            entity.world = self
            self.items.update({entity.name:entity})
        elif isinstance(entity,room):
            entity.world = self
            self.rooms.update({entity.name:entity})
    def entities(self,room_coords):
        target_room = self.rooms[room_coords]
        return_entities = []
        for c in self.characters.values():
            if c.location == room_coords:
                return_entities.append(c)
        for i in self.items.values():
            if i.location == room_coords:
                return_entities.append(i)
        return return_entities
    def act(self):
        for c in self.characters.values():
            the_situation = situation(self.entities(c.location))
            c.act(the_situation)
    def change_sublocation_x(self,entity,amount):
        if isinstance(entity,character):
            self.characters[entity.name].sublocation[0] += amount
        elif isinstance(entity,item):
            self.items[entity.name].sublocation[0] += amount
    def change_sublocation_y(self,entity,amount):
        if isinstance(entity,character):
            self.characters[entity.name].sublocation[1] += amount
        elif isinstance(entity,item):
            self.items[entity.name].sublocation[1] += amount
    def change_location_x(self,entity,amount):
        if isinstance(entity,character):
            old = self.characters[entity.name].location
            self.characters[entity.name].location = (old[0] + amount,old[1])
        if isinstance(entity,item):
            old = self.items[entity.name].location
            self.items[entity.name].location = (old[0] + amount,old[1])
    def change_location_y(self,entity,amount):
        if isinstance(entity,character):
            old = self.characters[entity.name].location
            self.characters[entity.name].location = (old[0],old[1] + amount)
        if isinstance(entity,item):
            old = self.items[entity.name].location
            self.items[entity.name].location = (old[0],old[1] + amount)
    def change_health(self,entity,amount):
        if isinstance(entity,character):
            entity.stats['wellness']['health'] += amount 
            if entity.stats['wellness']['health'] <= 0:
                print(entity.name +" has perished.")
                entity.die()
    def set_enemy(self,entity,enemy):
        if isinstance(entity,character):
            self.characters[entity.name].brain.enemy = enemy

class room:
    def __init__(self,coords,features,mapin):
        self.name = coords
        self.identity = features
        self.map = mapin
        self.world = None

class item:
    def __init__(self,name,features,stats):
        self.name = name
        self.identity = features
        self.stats = stats
        self.location = (0,0)
        self.sublocation = [0,0]
        self.avatar = '/'
        self.world = None

class brain:
    def __init__(self,choice='ai'):
        self.controller = choice
        self.controlled = None
        self.enemy = None
    def act(self,situation):
        player_commands = {'n':self.controlled.move_n,
                           's':self.controlled.move_s,
                           'w':self.controlled.move_w,
                           'e':self.controlled.move_e, ',':self.controlled.wait,
                           '?':self.controlled.status, 'i?':self.controlled.inv, 'e?':self.controlled.equip_check,
                           'ex':self.examine, 'con':self.consider,
                           '8':self.controlled.attack_n, 'an':self.controlled.attack_n,
                           '6':self.controlled.attack_e, 'ae':self.controlled.attack_e,
                           '4':self.controlled.attack_w, 'aw':self.controlled.attack_w,
                           '2':self.controlled.attack_s, 'as':self.controlled.attack_s,
                           'quit': exit}
        if self.controller == 'player':
            cycle = True
            while cycle:
                choice = input(self.controlled.name+"-: ")
                if choice in player_commands.keys():
                    try:
                        player_commands[choice]()
                    except:
                        player_commands[choice](situation)
                    cycle = False

        elif self.controller == 'ai':
            action_to_be = ''
            if len(situation.entities) > 1:
                if self.enemy:
                    target = self.enemy.sublocation
                    origin = self.controlled.sublocation
                    difference = [target[0]-origin[0],target[1]-origin[1]]
                    if abs(difference[0]) > 1:
                        if abs(difference[1]) > 1:
                            if abs(difference[0]) > abs(difference[1]):
                                if difference[0] < 0: self.controlled.move_w()
                                else: self.controlled.move_e()
                            else:
                                if difference[1] < 0: self.controlled.move_n()
                                else: self.controlled.move_s()
                        else:
                            if difference[0] < 0: self.controlled.move_w()
                            else: self.controlled.move_e()
                    else:
                        if abs(difference[1]) > 1:
                            if difference[1] < 0: self.controlled.move_n()
                            else: self.controlled.move_s()
                        else:
                            print("ATTACKING")
            if action_to_be == '':
                random.choice([self.controlled.move_n,self.controlled.move_s,self.controlled.move_e,self.controlled.move_w,self.controlled.wait])()
    def examine(self,situation):
        global pp
        choices = situation.entities
        print()
        print("Examine: \n")
        index = 0
        for c in choices:
            print(str(index)+" - "+c.name)
            index += 1
        choice = input("choice: ")
        pp.pprint(choices[int(choice)].identity)
    def consider(self,situation):
        global pp
        choices = []
        for i in situation.entities:
            if isinstance(i,character):
                choices.append(i)
        print()
        print("Consider: \n")
        index = 0
        for c in choices:
            print(str(index)+" - "+c.name)
            index += 1
        choice = input("choice: ")
        pp.pprint(choices[int(choice)].stats['wellness'])
    def calculate_damage(self):
        base_attack = self.controlled.stats['action']['physicality'] / 3
        bonus = 0
        rando = random.randint(0,self.controlled.stats['action']['physicality']) / 2 * (self.controlled.stats['action']['learnedness'] / 4)
        if self.controlled.equipped:
            for i in self.controlled.equipped:
                if 'damage' in i.stats['bonus'].keys():
                    bonus += i.stats['bonus']['damage']
        return base_attack + rando + bonus
        

class situation:
    def __init__(self,entities):
        self.entities = entities
        self.intentions = {}
        self.consequences = []
        self.resolved = False
    def update(self):
        for e in entities:
            if isinstance(e,character):
                e.act(self)

class display:
    def __init__(self,name):
        self.current_world = world()

        player = character(name,{'description':"The hero of this narrative. You should probably save the world or something."},
        {'social':{'malice':0,'charity':0,'wealth':100},
         'action':{'physicality':10,'learnedness':10,'guile':10},
         'wellness':{'health':10,'energy':10}},brain('player'))
        player.brain.controlled = player

        self.current_world.spawn(player)
        
        other = character('Bo',{'description':"Good ole Bo. He's a farmer."},
        {'social':{'malice':15,'charity':35,'wealth':60}, 'action':{'physicality':12,'learnedness':5,'guile':8}, 'wellness':{'health':30,'energy':10}},brain('ai'))
        other.brain.controlled = other
        other.sublocation[0] += 3
        self.current_world.spawn(other)

        self.current_room = self.current_world.rooms[player.location]

        self.update()

    def update(self):
        x_trace = 0
        y_trace = 0
        entities = self.current_world.entities(self.current_room.name)
        room_temp = self.current_room.map[:]
        rows = []
        current_row = ''
        placed_entities = []

        for e in entities:
            rows = []
            for y in room_temp:
                for x in y:
                    if e.sublocation == [x_trace,y_trace]:
                        current_row += e.avatar
                        placed_entities.append(e)
                    else:
                        current_row += x
                    x_trace += 1
                x_trace = 0
                rows.append(current_row)
                current_row = ''
                y_trace += 1
            y_trace = 0
            room_temp = rows[:]

        changes = False
        
        for i in entities:
            if i not in placed_entities:
                if i.sublocation[0] < 0:
                    self.current_world.change_sublocation_x(i,1)
                    changes = True
                elif i.sublocation[0] > len(self.current_room.map[0])-1:
                    self.current_world.change_sublocation_x(i,-1)
                    changes = True
                elif i.sublocation[1] < 0:
                    self.current_world.change_sublocation_y(i,1)
                    changes = True
                elif i.sublocation[1] > len(self.current_room.map)-1:
                    self.current_world.change_sublocation_y(i,-1)
                    changes = True

        if changes:
            self.update()
        else:
            for row in rows:
                print(row)

            self.current_world.act()


if __name__ == "__main__":
    name = input("Name: ")
    terminal = display(name)
    while True:
        terminal.update()

"""
stats:
    malice
    charity.
    wealth
    physicality
    learnedness
    guile
    health
    energy

example stat block:
    {'m':45,'c':20,'w':1090,
     'p':15,'l':10,'g':12,
 'h': |:34}
"""

"""
identity:
    age
    race
    appearance
"""
