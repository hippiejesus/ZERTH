import sys
import pprint

pp = pprint.PrettyPrinter(indent = 3)

start = ['----------------',
         '----------------',
         '----------------',
         '----------------',
         '----------------',
         '----------------',
         '----------------']

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
    def act(self,situation):
        self.brain.act(situation)
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

class world:
    def __init__(self):
        global start
        self.rooms = {(0,0):room((0,0),None,start)}
        self.characters = {}
        self.items = {}
    def spawn(self,entity):
        if isinstance(entity,character):
            self.characters.update({entity.name:entity})
        elif isinstance(entity,item):
            self.items.update({entity.name:entity})
        elif isinstance(entity,room):
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
            c.act(None)
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
        pass
    def change_location_y(self,entity,amount):
        pass

class room:
    def __init__(self,coords,features,mapin):
        self.name = coords
        self.identity = features
        self.map = mapin

class item:
    def __init__(self,name,features,stats):
        self.name = name
        self.identity = features
        self.stats = stats
        self.location = (0,0)
        self.sublocation = [0,0]
        self.avatar = '/'

class brain:
    def __init__(self,choice='ai'):
        self.controller = choice
        self.controlled = None
    def act(self,situation):
        player_commands = {'n':self.controlled.move_n,
                           's':self.controlled.move_s,
                           'w':self.controlled.move_w,
                           'e':self.controlled.move_e, ',':self.controlled.wait,
                           '?':self.controlled.status, 'i?':self.controlled.inv, 'e?':self.controlled.equip_check,
                           'quit': exit}
        if self.controller == 'player':
            cycle = True
            while cycle:
                choice = input(self.controlled.name+"-: ")
                if choice in player_commands.keys():
                    player_commands[choice]()
                    cycle = False

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

        player = character(name,None,
        {'social':{'malice':0,'charity':0,'wealth':100},
         'action':{'physicality':10,'learnedness':10,'guile':10},
         'wellness':{'health':10,'energy':10}},brain('player'))
        player.brain.controlled = player

        self.current_world.spawn(player)
        
        other = character('Bo',None,
        {'social':{'malice':15,'charity':35,'wealth':60}, 'action':{'physicality':10,'learnedness':10,'guile':10}, 'wellness':{'health':10,'energy':10}},brain('ai'))
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

        if not changes:
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
