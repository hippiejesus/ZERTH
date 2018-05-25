import master as m
import place as p
import being as b
import objects as o

name = input('Name: ')
m.current_region = p.region(coordinates = [0,0],environment = p.m.GRASS)

m.test_player = b.player(nickname = name)
m.placeBeing(m.test_player,0)

m.test_person = b.person(nickname = str(m.genCharName()))
m.placeBeing(m.test_person,58)


m.placeObj('wep_011',27)
m.placeObj('wep_011',98)
m.placeObj('wep_007',74)

m.main()