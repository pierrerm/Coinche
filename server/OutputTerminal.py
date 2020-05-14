# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:40:42 2019

@author: rthie
"""

import generical_function as generic
import coinche_constant as const




class OutputTerminal():
  "This manager is used to link the output to the core"

  @classmethod
  def display(cls,hand): 
    """
    display an array of cards
    """
    print("\n \n {:^15} \n".format(hand.name))
    for i in range(len(hand.cards)):
      print("{} : {:>2} de {} ".format(str(i+1),hand.cards[i].number,hand.cards[i].color))
    print()

  @classmethod
  def choose_card(cls,self,random): 
     """
     choose and return a card
     """
     while True :
         if not random : #TODO Change
           cls.display(self) #TODO Change
         card_position = generic.decision(liste_choix_possible=const.INTEGERS32[:len(self.cards)], random=random, question="Quelle carte ? 1ère, 2ème ? ")
         card_position = int(card_position)-1
         if card_position<len(self.cards) :
             if self.cards[card_position].rest:
                 return self.cards[card_position]

  def __init__(self):

    #Instance Attributes

    pass



#TESTS
    
if __name__=="__main__"   :

  pass



