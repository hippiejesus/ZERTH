import being as b
import random as r
import copy

global itemListPath,itemList
beingListPath = 'beingList1.txt'
beingList = dict()
global current,currentTag
current = b.being('')
currentTag = None

name = None
kind = None
durability = None
description = None
buffs = None

def ref(stem,change):
    if stem == 'name':
        current.name = change
    elif stem == 'nickname':
        if isinstance(current,b.person):
            current.nickname = change
    elif stem == 'strength':
        current.stats['Strength'] = int(change)
    elif stem == 'agility':
        current.stats['Agility'] = int(change)
    elif stem == 'intellect':
        current.stats['Intellect'] = int(change)
    elif stem == 'sense':
        current.stats['Sense'] = int(change)
    elif stem == 'wounds':
        current.stats['Wounds'] = int(change)
    elif stem == 'vitality':
        current.stats['Vitality'] = int(change)
    elif stem == 'discipline':
        current.stats['Discipline'] = int(change)
    elif stem == 'toughness':
        current.stats['toughness'] = int(change)
    elif stem == 'resistances':
        pass
    elif stem == 'inventory':
        pass
    elif stem == 'resources':
        pass
    elif stem == 'icon':
        current.icon = change
        
def listImport():
    global current,currentTag
    f = open(beingListPath,'r')
    for line in f.readlines():
        ls = line.split()
        if ls == []: pass
        elif ls[0] == '+':
            if ls[1] == 'person':
                current = b.person()
            elif ls[1] == 'plant':
                current = b.plant()
            elif ls[1] == 'animal':
                current = b.animal()
        elif ls[0] == 'vvv':
            currentTag = ls[1]
        elif ls[0] == '...':
                 
            save = copy.deepcopy(current)
            beingList.update({currentTag:save})
            currentTag = None
        else:
            le = line.split('=')
            tar = le[0].strip(' ')
            #print(tar)
            #print(tar in ref.keys())
            re= le[1][1:][:-1]
            ref(tar,re)
    f.close

"""print(itemList)
for item in itemList.values():
    print('\n\n')
    item.report()"""
    
def getBeingList(): return beingList
