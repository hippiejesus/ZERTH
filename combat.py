import random as r
import time

default_stats_person={'Strength':10,'Agility':15,'Intellect':15,
               'Sense':12,'Wounds':10,'Vitality':10, 'Discipline':'d8',
               'Toughness':0,'AC':0,'Resistances':{'Slashing':10},
               'Equipped':{},'Inventory':{}}

class combat:
    def __init__(self,combatants,location):
        self.combatants = combatants
        self.location = location
        for actor in self.combatants:
            actor.inCombat = True
            actor.currentCombat = self
        self.location.battle_list.append(self)
    def turn(self,actor,action):
        target = None
        for i in self.combatants:
            if i != actor: target = i
        if action == 'attack':
            attackerST = actor.stats['Strength']
            defenderST = target.stats['Strength']
            attackerAG = actor.stats['Agility']
            defenderAG = target.stats['Agility']
            attackerIN = actor.stats['Intellect']
            defenderIN = target.stats['Intellect']
            
            print(actor.nickname+' attacks '+target.nickname+'...')
            
            toHit = defenderAG+(.5*defenderIN)
            attackBonus = (.3*attackerST)+(.3*attackerAG)+(.5*attackerIN)
            attack = r.randint(0,20)+attackBonus
            print('toHit = '+str(toHit)+' attackBonus = '+str(attackBonus))
            
            time.sleep(1)
            print('...')
            print('attack == '+str(attack))                                                   
            time.sleep(2)
            
            if attack >= toHit:
                damage = 0
                weapons = []
                for item in actor.stats['Equipped'].values():
                    if item.kind == 'weapon':
                        weapons.append(item)
                        damageEquation = item.damage
                        equationSplit = damageEquation.split('+')
                        baseDamage = equationSplit[0].split('d')
                        for repeats in range(int(baseDamage[0])):
                            pendingDamage = r.randint(1,int(baseDamage[1]))
                            print(str(pendingDamage)+' '+item.name+' damage')
                            time.sleep(1)
                            damage += pendingDamage
                        equationSplit.pop(0)
                        for i in equationSplit:
                            if i == 'str':
                                pendingDamage = (actor.stats['Strength'] * .5)
                                damage += pendingDamage
                                print(str(pendingDamage)+' strength damage')
                                time.sleep(1)
                            elif i == '': pass
                            else: damage += int(i) ; print(str(i)+' bonus damage') ; time.sleep(1)
                if weapons == []:
                    pendingDamage = (actor.stats['Strength']*.1)+r.randint(0,3)
                    print(str(pendingDamage)+' unarmed damage') ; time.sleep(1)
                    damage += pendingDamage
                tVital = target.stats['Vitality']
                if tVital - damage < 0:
                    target.stats['Wounds'] -= abs(tVital-damage)
                    target.stats['Vitality'] = 0
                else:
                    target.stats['Vitality'] -= damage
                print('and hits for '+str(damage)+' damage!')
                print(target.nickname+': V='+str(target.stats['Vitality'])+' W='+str(target.stats['Wounds']))
            else:
                print('and misses...')
            time.sleep(3)
            if target.stats['Wounds'] <= 0:
                print(target.nickname+' has croaked!')
                target.icon = '%'
                target.nickname = 'Corpse of '+target.nickname
                target.isDead = True
                self.resolve()
                
    def resolve(self):
        for actor in self.combatants:
            actor.inCombat = False
            actor.currentCombat = None
        self.location.battle_list.remove(self)
        self.location = None
        self.combatants = None
