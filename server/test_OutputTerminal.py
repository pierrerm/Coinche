#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:48:39 2019

@author: rthiebaut
"""

import generical_function as generic
from Card import Card
from Hand import Hand
import coinche_constant as const

"""
Les tests générés ici sont réalisés depuis le plus haut level (les classes Hand game round ..)
"""

def test_display():

  mycard1=Card("7","carreau")
  mycard2=Card("7","coeur")
  pioche =[ Card(i,j) for j in const.COLORS[:4] for i in const.NUMBERS]
  mypioche=Hand(cards=pioche,name="pioche")
  myhand=Hand(name="Pli",cards=[mycard2,mycard1])
  myhand.display()
  mypioche.display()

def test_choose_card():

  pioche =[ Card(i,j) for j in const.COLORS[:4] for i in const.NUMBERS]
  mypioche=Hand(cards=pioche,name="pioche")

  for i in range (100):
    card=mypioche.choose_card()
    assert(card.rest)




if __name__=="__main__"   :
  generic.test("display",test_display)
  generic.test("choose_card",test_choose_card)

