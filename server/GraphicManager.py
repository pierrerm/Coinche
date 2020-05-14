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
  def choose_card(cls,hand,random): #UI
    """
    choose and return a card
    """
    if not cls.hidden :
      if cls.output=="terminal":
            return OutputTerminal.choose_card(hand,random)

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



