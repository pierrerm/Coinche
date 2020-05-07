#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:28:13 2019

@author: rthiebaut
"""

"""
Useful Function
"""
import random #use randrange
import sys
import time

def indice(liste,element): #trouve l'indice de l'élément dans la liste attention lelement doit etre present utiliser NameOfTheList.index
  for i,e in enumerate(liste):
      if e==element:
        return i


def question_ferme(proposition): #rajout dun quit
  """
  souhaitez vous "proposition" ? si oui -> vrai / si non -> false
  """
  while True :
       x=input("Souhaitez-vous %s ? oui/non " % proposition)
       if x=='quit':
           sys.exit()
       if x=='oui' or x=='non' :
           break
  if x=='oui':
      return True
  else :
      return False

def question_ouverte(question, liste_choix_possible) : #rajout dun quit
    """
    return une proposition qui reponds aux conditions requises
    """
    while True :
        proposition = input(question)
        if proposition=="quit":
            sys.exit()
        if proposition in liste_choix_possible :
            return proposition

def choix_aleatoire(liste_choix_possible) :
    """
    fais un choix aleatoire parmis ceux possibles
    """
    choix=random.randrange(len(liste_choix_possible))
    return liste_choix_possible[choix]

def decision(liste_choix_possible=[True,False], random=True, question="", ouverte=True):
    if random :
        return(choix_aleatoire(liste_choix_possible))
    else :
        if ouverte:
            return(question_ouverte(question, liste_choix_possible))
        else :
            return (question_ferme(question))

def time_check(f,nb_iter=100,*args,**kwargs):
  """
  return the elapsed time during the computation of n times the function
  """
  total_time=0
  for i in range(nb_iter):
    tic = time.clock()
    f(**kwargs)
    toc = time.clock()
    total_time+=toc-tic
  return total_time

def test(test_name,test_function,*args,**kwargs):
  print("Testing ", test_name)
  test_function(*args,**kwargs)
  print("Test OK",end ="\n"*2)
  return 0


