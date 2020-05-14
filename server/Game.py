#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:49:30 2019

@author: rthiebaut
"""
from Round import Round
from Hand import Hand
from Card import Card

import generical_function as generic
import coinche_constant as const
import random as rand
from GraphicManager import GraphicManager




class Game():

  def __init__(self, team_names=["e1","e2"], player_names=["j1","j2","j3","j4"], player_bots=[False,True,True,True],
                score_limit=2000,hidden=False,
                difficulty="beginner"):

      GraphicManager.hidden=hidden

      self.data= {"team_names":team_names, "player_names":player_names, "player_bots":player_bots}

      self.round=Round(team_names=self.data["team_names"], player_names=self.data["player_names"], player_bots=self.data["player_bots"],
                number=0,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]),
                difficulty=difficulty)

      self.limit=score_limit
      self.score={team_names[0]:0,team_names[1]:0}

      self.difficulty=difficulty

  def result(self): # normalement mise nest pas char
      total_points=self.round.teams[0].pli.count_points()+self.round.teams[1].pli.count_points()
      assert(total_points==162 or total_points==182) #compte les points par équipe pas encore de 10 de der
      if self.round.surcoinche :
          multiplicator = 4
      elif self.round.coinche :
          multiplicator = 2
      else :
          multiplicator =1

      for team in self.round.teams :
          if team.bet != None:
              capot= team.bet==250 and len(team.pli.cards)==32 #bool capot
              generale=(team.players[0].plis==8 and team.players[0].generale==True ) or ( team.players[1].plis==8 and team.players[1].generale==True) #bool generale

              #cas 1 : réussite du contrat
              if team.bet<=team.pli.points or capot or generale : #faire cas général : compteur de pli gagné par player


                #cas 1.1 : coinché ou surcoinché
                if self.round.coinche :
                    self.score[team.name] += team.bet*multiplicator # seulement points contrats
                    self.score[self.round.teams[(team.number+1)%2].name] += 0 #points defense

                #cas 1.2 : normal
                else :
                    self.score[team.name] += team.bet # seulement points contrats
                    self.score[self.round.teams[(team.number+1)%2].name] += self.round.teams[(team.number+1)%2].pli.points #points defense

                #It's a success
                GraphicManager.result(team=team,win=True,score=self.score) #UI



              #cas 2 : échec du contrat
              else :
                  self.score[self.round.teams[(team.number+1)%2].name] += 160*multiplicator
                  
                  #It's a fail 
                  GraphicManager.result(team=team,win=False,score=self.score) #UI





  def end_round(self) :
       self.result()
       for team in self.score:
         if self.score[team]>self.limit: #error
            GraphicManager.end(team=team,game=self) #UI
            return False
       return True

  def new_round(self,round_number) :

    pioche=Hand(name="pioche",cards=[],sort=False)
      # the last round was played
    pioche+=self.round.teams[0].pli
    pioche+=self.round.teams[1].pli
      # the last round wasn't played
    players_in_order=self.round.getPlayersInOrder() #changer ordre a chaque manche ????
    for player in players_in_order :
      pioche+=player.Hand
    assert(pioche.rest["cards"]==32)

    # Reset trump and value information of the previous round
    for card in pioche.cards : # it seems to work
      card.reset()

    self.round=Round(team_names=self.data["team_names"], player_names=self.data["player_names"], player_bots=self.data["player_bots"],
                        number=round_number,pioche=pioche,
                        difficulty=self.difficulty)


  def reinitialize(self):
    self.new_round(round_number=0)
    self.score={self.data["team_names"][0]:0,self.data["team_names"][1]:0}


  def run(self):
     while True : #game root
       round_number = 0 # The first Round is the Round 1
       played = True
       while True: # round root
         while True : #round of assertion : is a trump is taken or not
           round_number+=1
           self.new_round(round_number)
           played=self.round.run()
           if played :
             break
         if not self.end_round():
           break
       #this trick automatize the launch of a new game if all players are bots
       if GraphicManager.newGame(isBot= ( 2+sum(self.data["player_bots"]) ) %5): #UI
         break
       else :
         self.reinitialize()

def random_test():
  mygame=Game(player_bots=[True]*4,hidden=True,difficulty="advanced")
  mygame.run()

if __name__=="__main__"   :

  print("random test")
  for i in range(500):
    random_test()
  print("test OK")

