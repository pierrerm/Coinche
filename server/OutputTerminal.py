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
  def choose_card(cls,hand,isBot): 
     """
     choose and return a card
     """
     while True :
         card_position = generic.decision(liste_choix_possible=const.INTEGERS32[:len(hand.cards)], random=isBot, question="Quelle carte ? 1ère, 2ème ? ")
         card_position = int(card_position)-1
         if card_position<len(hand.cards) :
             if hand.cards[card_position].rest:
                 return hand.cards[card_position]

  @classmethod
  def chooseTrump(cls,round,hidden): # pensez a display avant surcoinche empecher danooncer 170 180 tout trump sans trump
     """
     fix the trump and return true if someone didnt pass his turn
     """
     j=round.getPlayersInOrder()
     bet=0
     annonce_actuelle=-1
     turn=0
     while turn!=4 and bet!='generale' and not round.coinche:
        for player in j:
           if turn==4 or bet=='generale' or round.coinche:
              break
           else:
              if not hidden :
                if not player.random :
                  cls.display(player.Hand) #UI

              if not generic.decision(random=player.random, question='annoncer', ouverte=False): #local variable referenced before assignment
                 turn+=1

              else:
                 turn=1

                 round.trump=generic.decision(const.COLORS, random=player.random, question ="Choisir la couleur d'atout : %s " % const.COLORS)

                 while True :

                    bet = generic.decision(const.ANNOUNCES, random=player.random, question="Choisir la hauteur d'annonce : %s " % const.ANNOUNCES )
                    annonce_voulue=const.ANNOUNCES.index(bet)
                    if annonce_voulue>annonce_actuelle :
                        annonce_actuelle=annonce_voulue

                        if not hidden :  #GRAPHIC
                          print(' {} prend à {} {} !'.format(player.name,bet,round.trump))

                        break

                 round.teams[player.team].bet=bet #fixe la bet de lteam attention bet est un char
                 round.teams[(player.team+1)%2].bet=None
                 if bet == "generale":
                     player.generale=True
                 for coincheur in round.teams[(player.team+1)%2].players:

                   if not hidden :  #GRAPHIC
                     if not coincheur.random :
                      coincheur.Hand.display()

                   if not round.coinche :
                      round.coinche=generic.decision(random=coincheur.random, question='coincher sur {} {} ?'.format(bet,round.trump), ouverte=False)
                      if round.coinche:
                         if not hidden : #GRAPHIC
                           print(' {} coinche sur {} {} !'.format(coincheur.name,bet,round.trump))
                         for surcoincheur in round.teams[player.team].players:

                           if not hidden : #GRAPHIC
                             if not surcoincheur.random :

                              surcoincheur.Hand.display()

                           if not round.surcoinche :
                               round.surcoinche=generic.decision(random=surcoincheur.random, question='surcoincher sur {} {} ?'.format(bet,round.trump), ouverte=False)
                               if round.surcoinche :
                                 if not hidden : #GRAPHIC
                                   print(' {} surcoinche sur {} {} !'.format(surcoincheur.name,bet,round.trump))

     if (round.trump==None):
          return False

     if not hidden :  #GRAPHIC
       for team in round.teams :
            if team.bet!=None:
                print("L'équipe '{}' a pris {} à {} !!!".format(team.name, team.bet, round.trump))

     return True


  @classmethod
  def result(cls,team,win,score): 
    """
    display the result of the round
    """
    if win :
      print("l'équipe {} a réussit son contrat".format(team.name))
    else :
      print("l'équipe {} a chuté".format(team.name))
    
    print(score)

  @classmethod
  def end(cls,team,game): 
    """
    display the end of the game
    """

    print(game.round.trump, game.round.teams[0].bet, game.round.teams[1].bet)
    print( " l'équipe {} a gagné avec {} ".format(team, game.score))

  @classmethod
  def newGame(cls,isBot): 
    """
    Ask for a new game
    """
    return generic.decision(question="une nouvelle partie", ouverte=False,random=isBot)

  @classmethod
  def winner(cls,name,number,color) :
    """
    display the result of the pli
    """
    print("{} a gagné avec le {} de {}".format(name,number,color))




  def __init__(self):

    #Instance Attributes

    pass



#TESTS
    
if __name__=="__main__"   :

  pass



