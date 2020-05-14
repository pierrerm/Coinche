# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:40:42 2019

@author: rthie
"""

import generical_function as generic
import coinche_constant as const
from OutputTerminal import OutputTerminal



class GraphicManager():
  "This manager is used to link the output to the core"

  #Class Attributes

  output = const.OUTPUT[0] # Should be terminal

  # showing things or not
  hidden = False


  @classmethod
  def setOutput(cls, newOutput):
    assert(newOutput in const.OUTPUT)
    GraphicManager.output =newOutput

  @classmethod
  def display(cls,hand): 
     """
     display an array of cards
     """
     if not cls.hidden :
      if cls.output=="terminal":
        OutputTerminal.display(hand)

      if cls.output=="terminal":
        pass

  @classmethod
  def result(cls,team,win,score): 
     """
     display the result of the round
     """
     if not cls.hidden :
      if cls.output=="terminal":
        OutputTerminal.result(team,win,score)

      if cls.output=="terminal":
        pass

  @classmethod
  def winner(cls,name,number,color) :
     """
     display the result of the pli
     """
     if not cls.hidden :
      if cls.output=="terminal":
        OutputTerminal.winner(name,number,color)

      if cls.output=="terminal":
        pass



  @classmethod
  def end(cls,team,game): 
    """
    display the end of the game
    """

    if not cls.hidden :
      if cls.output=="terminal":
        OutputTerminal.end(team,game)

      if cls.output=="terminal":
        pass

  @classmethod
  def newGame(cls,isBot): 
    """
    Ask for a new game
    """
    if cls.output=="terminal":
          return OutputTerminal.newGame(isBot)

    if cls.output=="terminal":
      pass
  @classmethod
  def choose_card(cls,hand,isBot): #UI
    """
    choose and return a card
    """
    if cls.output=="terminal":
          return OutputTerminal.choose_card(hand,isBot)

    if cls.output=="terminal":
      pass

  @classmethod
  def chooseTrump(cls,round): # pensez a display avant surcoinche empecher danooncer 170 180 tout trump sans trump
    """
    fix the trump and return true if someone didnt pass his turn
    """
    if cls.output=="terminal":
          return OutputTerminal.chooseTrump(round,cls.hidden)

    if cls.output=="terminal":
      pass




  def __init__(self):

    #Instance Attributes

    pass



#TESTS

def test_setOuput():

  mymanager = GraphicManager()
  mymanager.setOutput("graphic")
  assert(GraphicManager.output=="graphic")

  GraphicManager.setOutput("terminal")
  assert(mymanager.output=="terminal")

  #checking that our assertion works
  occuranceException=False
  try:
    GraphicManager.setOutput("bill")
  except:
   occuranceException=True
  assert(occuranceException)
    
if __name__=="__main__"   :

  generic.test("setOutput",test_setOuput)



