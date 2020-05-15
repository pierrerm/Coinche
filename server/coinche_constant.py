#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:32:38 2019

@author: rthiebaut
"""

"""
Constantes
"""

NUMBERS=['7', '8', '9', 'V', 'D', 'R', '10', 'As'] #As=A
COLORS=['coeur', 'pique', 'carreau', 'trefle',  'sans atout', 'tout atout']
GAMEMODES=["normal","atout","sans atout","tout atout"]
#attention erreur

normal=[0, 0, 0, 2, 3, 4, 10, 11]
atout=[0, 0, 14, 20, 3, 4, 10, 11]
sansatout=[0, 0, 0, 2, 3, 4, 10, 19]
toutatout=[0, 0, 9, 14, 1, 2, 5, 7]
ConstructionPoints=[normal,atout,sansatout,toutatout]

POINTS={}
j=0
for mode in GAMEMODES :
    POINTS[mode]={}
    for i in range(8):
        POINTS[mode][NUMBERS[i]]=ConstructionPoints[j][i]
    assert(len(POINTS[mode])==8)
    j+=1
assert(4*sum(POINTS[GAMEMODES[3]].values())==152)
assert(4*sum(POINTS[GAMEMODES[2]].values())==152)
assert(3*sum(POINTS[GAMEMODES[0]].values())+sum(POINTS[GAMEMODES[1]].values())==152)


ANNOUNCES=[str(80+10*i) for i in range(11)]
ANNOUNCES.append('capot')
ANNOUNCES.append('generale')
INTEGERS32=[]
for i in range(1,33):
    INTEGERS32.append(str(i))
    
TRUMPORDER=['7', '8', 'D', 'R', '10', 'As', '9', 'V']

OUTPUT=["terminal","web"]