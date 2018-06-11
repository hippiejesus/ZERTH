#Being.py
#Handles player and NPCs, as well as any beasties and monsters that may be lurking about.
import random as r
import copy

needsReferences = nr = dict() #references to objects that
                              #fill a particular need
 
 
default_stats_person={'Strength':10,'Agility':15,'Intellect':15,
               'Sense':12,'Wounds':10,'Vitality':10, 'Discipline':'d8',
               'Toughness':0,'AC':0,'Resistances':{'Slashing':10},
               'Equipped':{},'Inventory':{},'Resources':{}} 
               
default_stats_plant={'Strength':1,'Agility':0,'Intellect':1,
               'Sense':5,'Wounds':2,'Vitality':2,
               'Toughness':0,'AC':0,'Resistances':{'Weather':50},'Edible':False,'Resources':{}} 
               
default_stats_animal={'Strength':10,'Agility':15,'Intellect':15,
               'Sense':12,'Wounds':10,'Vitality':10, 'Discipline':'d8',
               'Toughness':0,'AC':0,'Resistances':{'Slashing':10},
               'Equipped':{},'Inventory':{},'Resources':{}} 
               
        
class being:
    def __init__(self,stats,name = 'Unknown'):
        self.stats = stats
        self.name = name
        self.amI = ['being']
        self.icon = '!'
        self.coord = 0
        self.actions = []
        
        self.satiation = 50
        self.hydration = 70
        self.priorities = ['survival']
        self.needs = ['food','water','air']
        
        self.wander_frequency = 6
        self.hasHome = False
        self.targetResource = None
        
        self.isResource = False
        self.resourceType = None
        
        self.inCombat = False
        self.currentCombat = None
        self.combatAction = None
        
        self.passable = False
        
        self.isDead = False
        
    def act(self):
        if self.actions != []:
            action = self.actions[0]
            self.actions.pop(0)
            return action
            
    def consider(self):
        if self.priorities != []:
            if 'wander' in self.priorities:
                if r.randint(0,10) > self.wander_frequency:
                    self.actions.append(['move',r.choice(['q','w','e','d','c','x','z','a'])])
                    
            if 'survival' in self.priorities:
                if self.hydration < 55:
                    self.actions.append(['seek','water'])
                    self.targetResource = 'water'
                elif self.satiation < 55:
                    self.actions.append(['seek','food'])
                    self.targetResource = 'food'
                elif self.hasHome == False:
                    self.actions.append(['seek','shelter'])
                    self.targetResource = 'shelter'
                else: self.targetResource = None
            

        
class person(being):
    def __init__(self,name = 'Human',nickname='Unknown',
                 stats=default_stats_person):
        being.__init__(self,stats,name)
        self.amI.append('person')
        self.discipline = 8
        self.nickname = nickname
        self.icon = nickname[0]
        self.needs.append('shelter')
        self.needs.append('clothing')
        print('test person')
        
    """def fillNeeds(self):
    global nr
        for category in self.needs:
            catList = nr[category]"""
            
class player(person):
    def __init__(self,name='Human',nickname='Unknown',stats=copy.deepcopy(default_stats_person)):
        person.__init__(self,name,nickname,stats)
        self.amI.append('player')
        self.icon = '@'
        self.seen = []
        self.stats = stats
        print('test player')
        
class npc(person):
    def __init__(self,name='Human',nickname='Unknown',stats=copy.deepcopy(default_stats_person)):
        person.__init__(self,name,nickname,stats)
        self.amI.append('npc')
        print('test npc')
        self.mood = 'Fair'
        self.stats = stats
        self.roles = []
        
class animal(being):
    def __init__(self,name='Animal',stats=copy.deepcopy(default_stats_animal)):
        being.__init__(self,name,stats)
        self.amI.append('animal')
        
        name = self.stats
        stats = self.name
        self.name = name
        self.stats = stats
        self.roles = []
        
        print('test beast')
        
class plant(being):
    def __init__(self,name='Plant',stats=copy.deepcopy(default_stats_plant)):
        being.__init__(self,name,stats)
        self.amI.append('plant')
        self.icon = '&'
        
        name = self.stats
        stats = self.name
        self.name = name
        self.stats = stats
        self.needs.append('light')
        
        print('test plant')
 
"""       
class npc_hostile(npc):
    def __init__(self):
        npc.__init__(self)
        self.amI.append('hostile')
        print('test npc_hostile')
        
class npc_commoner(npc):
    def __init__(self):
        npc.__init__(self)
        self.amI.append('commoner')
        print('test npc_commoner')
        
class npc_military(npc):
    def __init__(self):
        npc.__init__(self)
        self.amI.append('military')
        print('test npc_military')
"""
def test_player():
    test = player()

    print('A '+test.name+' called '+test.nickname+'\nWith the following stats!\n'+str(test.stats))


