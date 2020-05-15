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
  def update(cls): # TODO
    """
    send informations to update the display
    """
    pass

  @classmethod
  def choose_card(cls,hand,isBot):  # TODO
     """
     choose and return a card
     """
     return 0

  @classmethod
  def chooseTrump(cls,round,hidden): #TODO
     """
     fix the trump and return true if someone didnt pass his turn
     """
     return False


  @classmethod
  def newGame(cls,isBot): #TODO
    """
    Ask for a new game and return true if the player wants to replay
    """
    return False





  def __init__(self):

    #Instance Attributes

    pass



#TESTS
    
if __name__=="__main__"   :

  pass



