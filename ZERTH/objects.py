#Object.py
#Handles items, furniture, weapons, armor, and inventions


class item:
    def __init__(self,name,kind=None,durability=None,
                 description=None,buffs=dict(),
                 debuffs=dict(),damage=None,
                 damageType=None,damageReductions=dict(),
                 coverage=None,weight=0.00,speed=0,
                 icon = '$',slots=None):
        self.name = name
        self.kind = kind
        self.durability = durability
        self.description = description
        self.buffs = buffs
        self.debuffs = debuffs
        self.damage = damage
        self.damageType = damageType
        self.damageReductions = damageReductions
        self.coverage = coverage
        self.weight = weight
        self.speed = speed
        self.icon = icon
        self.slots = slots
        
        self.location = None #location object reference
        self.coord = 0
        
        self.isEquipped = False

    def materialize(self,location,coord):
        self.location = location
        self.coord = coord
        
    def report(self):
        print(str(self.name))
        print(str(self.kind) + ' --> ' + str(self.slots))
        print(str(self.description))
        print('\nDurability: '+str(self.durability))
        print('Damage: '+str(self.damage))
        print('Damage Type: '+str(self.damageType))
        print('\nCoverage: '+str(self.coverage))
        print('Damage Reductions: '+str(self.damageReductions))
        print('\nSpeed: '+str(self.speed))
        print('Weight: '+str(self.weight))
        print('\nBuffs: '+str(self.buffs))
        print('Debuffs: '+str(self.debuffs))
        print('\nIcon: '+str(self.icon))
        

class resource:
    def __init__(self,name,kind=None,quality=0.00,
                 quantity=0.00,unitSize=0.00,
                 targetNeed = None):
        self.name = name
        self.kind = kind
        self.quality = quality
        self.quantity = quantity
        self.unitSize = unitSize
        self.targetNeed = targetNeed

        self.location = None
        self.coord = 0

    def materialize(self,location,coord):
        self.location = location
        self.coord = coord

    def harvest(self,quantity):
        if self.quantity - quantity >= 0.00:
            self.quantity -= quantity
        else: return False
        if self.quantity <= 0:
            self.location = None
            self.coord = 0
            return 'depleted'
        else: return True
