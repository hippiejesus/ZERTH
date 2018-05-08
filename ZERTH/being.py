#Being.py
#Handles player and NPCs, as well as any beasties and monsters that may be lurking about.
 
default_stats_person={'Strength':10,'Agility':15,'Intellect':15,
               'Sense':12,'Wounds':10,'Vitality':10, 'Discipline':'d8',
               'Toughness':0,'AC':0,'Resistances':{'Slashing':10},
               'Equipped':['Shirt','Pants'],'Inventory':{}} 
               
default_stats_plant={'Strength':1,'Agility':0,'Intellect':1,
               'Sense':5,'Wounds':2,'Vitality':2,
               'Toughness':0,'AC':0,'Resistances':{'Weather':50}} 
               
default_stats_animal={'Strength':10,'Agility':15,'Intellect':15,
               'Sense':12,'Wounds':10,'Vitality':10, 'Discipline':'d8',
               'Toughness':0,'AC':0,'Resistances':{'Slashing':10},
               'Equipped':['Shirt','Pants'],'Inventory':{}} 
               
        
class being:
    def __init__(self,stats,name = 'Unknown'):
        self.stats = stats
        self.name = name
        self.amI = ['being']
        self.icon = '!'
        self.coord = 0
        
        self.satiation = 100
        self.hydration = 100
        self.interests = []

        
class person(being):
    def __init__(self,name = 'Human',nickname='Unknown',
                 stats=default_stats_person):
        being.__init__(self,stats,name)
        self.amI.append('person')
        self.discipline = 8
        self.nickname = nickname
        self.icon = nickname[0]
        print('test person')
        
class player(person):
    def __init__(self,name='Human',nickname='Unknown',stats=default_stats_person):
        person.__init__(self,name,nickname,stats)
        self.amI.append('player')
        self.icon = '@'
        self.seen = []
        print('test player')
        
class npc(person):
    def __init__(self,name='Human',nickname='Unknown',stats=default_stats_person):
        person.__init__(self,name,nickname,stats)
        self.amI.append('npc')
        print('test npc')
        self.mood = 'Fair'
        
class animal(being):
    def __init__(self,name='Animal',stats=default_stats_animal):
        being.__init__(self,name,stats)
        self.amI.append('animal')
        
        name = self.stats
        stats = self.name
        self.name = name
        self.stats = stats
        
        print('test beast')
        
class plant(being):
    def __init__(self,name='Plant',stats=default_stats_plant):
        being.__init__(self,name,stats)
        self.amI.append('plant')
        self.icon = '&'
        
        name = self.stats
        stats = self.name
        self.name = name
        self.stats = stats
        
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


