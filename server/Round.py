#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:30:05 2019

@author: rthiebaut
"""
import coinche_constant as const
import generical_function as generic
from Hand import Hand
from Card import Card
from Team import Team
import random as rand
from Bot import Bot
from AdvancedBot import AdvancedBot


class Round():
  """
  One Round of coinche
  """
  def __init__(self, team_names, player_names, player_bots,
               number,pioche, hidden=False,
               difficulty="beginner"): # e1 et e2 inutiles

    self.number=number 
    self.trump=None #trump of the round
    self.coinche=False #indicator of coinche
    self.surcoinche=False
    self.pli=Hand(name="Pli in progress",cards=[], sort=False)
    assert(self.pli.rest["cards"]==0)
    self.pioche=pioche

    if self.number==0 :
      players_cards=self.random_draw()
    else :
      players_cards=self.classic_draw()

    #bots creation

    self.bots={}

    if difficulty =="beginner" :
      for playerNumber in range(4):
        if player_bots[playerNumber] :
          self.bots[player_names[playerNumber]]=Bot(players_cards[playerNumber],
                   name=player_names[playerNumber],
                   allyName=player_names[(playerNumber+2)%4],
                   ennemyNames=[player_names[(playerNumber+1)%4],player_names[(playerNumber+3)%4]])


    if difficulty == "advanced" :

      for playerNumber in range(4):
        if player_bots[playerNumber] :
          self.bots[player_names[playerNumber]]=AdvancedBot(players_cards[playerNumber],
                   name=player_names[playerNumber],
                   allyName=player_names[(playerNumber+2)%4],
                   ennemyNames=[player_names[(playerNumber+1)%4],player_names[(playerNumber+3)%4]])



    self.teams=[Team(team_name=team_names[0], team_number=0,
                      j1_name=player_names[0], j1_random=player_bots[0], j1_cards=players_cards[0],
                      j2_name=player_names[2], j2_random=player_bots[2], j2_cards=players_cards[2]),
              Team(team_name=team_names[1], team_number=1,
                      j1_name=player_names[1], j1_random=player_bots[1], j1_cards=players_cards[1],
                      j2_name=player_names[3], j2_random=player_bots[2], j2_cards=players_cards[3])]

    self.hidden=hidden



  def random_draw(self):
    """
    #draw randomly in an array of cards
    """
    players=list()
    for nb_player in range(4):
      player=list()
      for nb_card in range(8):
        card=self.pioche.choose_card(random=True)
        card.rest=False
        player.append(card)
      players.append(player)

    for player in players:
      for card in player:
        card.rest=True

    self.pioche.reinitialize()
    return players



  def classic_draw(self, cut=False):
    """
    simulate the classic distribution in 3 3 2 self.pioche must countain the card in the rigth order
    """
    if cut :
      k=rand.randrange(32)#random cut the kieme card become the first the k-1 ieme become the last

      self.pioche.cards = self.pioche.cards[k:] + self.pioche.cards[:k]


    players=[(self.pioche.cards[3*i:3*i+3]+self.pioche.cards[3*i+12:3*i+15]+self.pioche.cards[2*i+24:2*i+26])
            for i in range(4)]

    self.pioche.reinitialize()
    return players



  def getPlayersInOrder(self): #TODO Test this method graphicaly to check everything is fine
    """
    Return an array of four players ordained according to the current round
    This method is basically used to shift the first player each round
    """
    players=[self.teams[0].players[0],  self.teams[1].players[0], self.teams[0].players[1], self.teams[1].players[1]]

    #This little trick should shift the first player every round 
    return [ players[ ( i + self.number-1 ) % 4 ] for i in range(4) ]

    


  #TODO : Remove it must be javascript
  def choose_trump(self): # pensez a display avant surcoinche empecher danooncer 170 180 tout trump sans trump
     """
     fix the trump and return true if someone didnt pass his turn
     """
     j=self.getPlayersInOrder()
     bet=0
     annonce_actuelle=-1
     turn=0
     while turn!=4 and bet!='generale' and not self.coinche:
        for player in j:
           if turn==4 or bet=='generale' or self.coinche:
              break
           else:
              if not self.hidden :  #GRAPHIC
                player.Hand.display(player.random)

              if not generic.decision(random=player.random, question='annoncer', ouverte=False): #local variable referenced before assignment
                 turn+=1

              else:
                 turn=1

                 self.trump=generic.decision(const.COLORS, random=player.random, question ="Choisir la couleur d'trump : %s " % const.COLORS)

                 while True :

                    bet = generic.decision(const.ANNOUNCES, random=player.random, question="Choisir la hauteur d'annonce : %s " % const.ANNOUNCES )
                    annonce_voulue=const.ANNOUNCES.index(bet)
                    if annonce_voulue>annonce_actuelle :
                        annonce_actuelle=annonce_voulue

                        if not self.hidden :  #GRAPHIC
                          print(' {} prend à {} {} !'.format(player.name,bet,self.trump))

                        break

                 self.teams[player.team].bet=bet #fixe la bet de lteam attention bet est un char
                 self.teams[(player.team+1)%2].bet=None
                 if bet == "generale":
                     player.generale=True
                 for coincheur in self.teams[(player.team+1)%2].players:

                   if not self.hidden :  #GRAPHIC
                     coincheur.Hand.display(coincheur.random)

                   if not self.coinche :
                      self.coinche=generic.decision(random=coincheur.random, question='coincher sur {} {} ?'.format(bet,self.trump), ouverte=False)
                      if self.coinche:
                         if not self.hidden : #GRAPHIC
                           print(' {} coinche sur {} {} !'.format(coincheur.name,bet,self.trump))
                         for surcoincheur in self.teams[player.team].players:

                           if not self.hidden : #GRAPHIC
                             surcoincheur.Hand.display(surcoincheur.random)

                           if not self.surcoinche :
                               self.surcoinche=generic.decision(random=surcoincheur.random, question='surcoincher sur {} {} ?'.format(bet,self.trump), ouverte=False)
                               if self.surcoinche :
                                 if not self.hidden : #GRAPHIC
                                   print(' {} surcoinche sur {} {} !'.format(surcoincheur.name,bet,self.trump))

     if (self.trump==None):
          return False

     if not self.hidden :  #GRAPHIC
       for team in self.teams :
            if team.bet!=None:
                print("L'équipe '{}' a pris {} à {} !!!".format(team.name, team.bet, self.trump))

     return True



  def cards_update(self): #memory leak => the next round will start with a pli of 40 cards for no reason
    """
    Update the cards after the trump color is choosen
    """
    players=self.getPlayersInOrder()
    #normal
    if self.trump in const.COLORS[:4]:

        for j in players:
            belote=0
            for card in j.Hand.cards:
                if card.color==self.trump:
                    card.trump=True
                    card.value=const.TRUMPORDER.index(card.number)
                    card.points=const.POINTS[const.GAMEMODES[1]][card.number]
                    if card.number=="R" or card.number=="D":
                        belote+=1
                        if belote==2:
                            if not self.hidden :  #GRAPHIC
                              print("le joueur {} a la belote".format(j.name)) # do not tell it right away
                            self.teams[j.team].pli.points+=20

                else :
                    card.value=const.NUMBERS.index(card.number)
                    card.points=const.POINTS[const.GAMEMODES[0]][card.number]
    #sans trump
    elif self.trump==const.COLORS[4]:
        for j in players :
            for card in j.Hand.cards:
                card.value=const.NUMBERS.index(card.number)
                card.points=const.POINTS[const.GAMEMODES[2]][card.number]

    #tout trump
    elif self.trump==const.COLORS[5]:
        for j in players :
            for card in j.Hand.cards:
                card.value=const.TRUMPORDER.index(card.number)
                card.points=const.POINTS[const.GAMEMODES[3]][card.number]

    total_points=0

    for team in self.teams: #associe la bet a un nombre de POINTS
        if team.bet!= None:
            if team.bet=='capot':
                team.bet=250
            elif team.bet=='generale':
                team.bet=500
            else :
                team.bet=int(team.bet)

    for j in players: #donne le nombre des POINTS de chaque Hand nest pas mis a jour par la suite


      total_points+=j.Hand.count_points()

    assert(total_points==152)


  def allowed_cards(self, choosen_color, j):
      """
      return cards allowed to play by the player who has to play
      """

      #cas 1 : la color demandée est trump
      if choosen_color==self.trump :

          #cas 1.1 : a de ltrump
          if j.Hand.rest[choosen_color]!=0 :
              trumps=[]

          #cas 1.11 : trump plus fort
              for carte in j.Hand.cards :
                  if carte.trump and carte.number!= None and carte.value > self.pli.cards[self.pli.winner()].value : #il faut checké que les cards sont présentes
                      trumps.append(carte)

              if len(trumps)!=0:
                  return Hand("Cards allowed",cards=trumps)

          # cas 1.12 : pas d'trumps plus forts

              return j.Hand.color(choosen_color)

          #cas 1.2 pas d'trump
          return Hand("Cards allowed",cards=j.Hand.cards)
      #cas 2 : la color demandée n'est pas ltrump

      #case 2.1 : a la color demandée
      if j.Hand.rest[choosen_color]!=0 :
          return j.Hand.color(choosen_color)

      #cas 2.2 : n'a  pas la color demandée

      #cas 2.21 : a trump
      if self.trump in const.COLORS[:4]:

          #cas 2.211 : le partenaire mène
          if self.pli.winner()%2==len(self.pli.cards)%2: #permet de se defausser sur partenaire
             return Hand("Cards allowed",cards=j.Hand.cards)


         #cas 2.212 : on doit couper
          if j.Hand.rest[self.trump]!=0 :
              return j.Hand.color(self.trump)

      #cas 2.22 pas dtrump
      return Hand("Cards allowed",cards=j.Hand.cards)




  def play_pli(self, players, pli_number): 
      """
      prends en entrée le tableau ORDONNEE des players de ce pli et le renvoi réordonné
      """

      #la meilleure card est le 1er joueur pour l'ini

      choosen_color=players[0].Hand.play_card( self.pli, players[0].Hand.choose_card(random=players[0].random))

      for j in players[1:]:
          if not self.hidden :#GRAPHIC
            self.pli.display(j.random)
          allowed_hand=self.allowed_cards( choosen_color, j)
          choosen_card=allowed_hand.choose_card(random=j.random)           # trois lignes a verifier
          j.Hand.play_card( self.pli, choosen_card)
      if not self.hidden :# GRAPHIC
        self.pli.display(self.hidden)

      winner=self.pli.winner()

      if not self.hidden :#GRAPHIC
          print("{} a gagné avec le {} de {}".format(players[winner].name, self.pli.cards[winner].number , self.pli.cards[winner].color ))
      new_order=[players[winner],players[(winner+1)%4], players[(winner+2)%4] ,players[(winner+3)%4]]
      players[winner].plis+=1
      self.teams[players[winner].team].pli+=self.pli #reinitialise le pli
      assert(self.pli.rest["cards"]==0)

       #compter 10 de der
      if pli_number==8 :
          self.teams[players[winner].team].pli.points+=10

      return new_order

  def run(self):
    """
    Run the round
    """
    if self.choose_trump() : #choisir valeur par defaut pour les test
      players_in_order=self.getPlayersInOrder() #changer ordre a chaque manche ????
      self.cards_update()
      for i in range(8):
        if not self.hidden: #GRAPHIC
            print("pli {} : \n \n".format(i))
        players_in_order=self.play_pli( players=players_in_order, pli_number=i+1) #erreur dans le decompte des plis confusion avec les tas player bug a iteration2 a priori fonctionne : confusion entre la position dans la main et celles des cartes possibles
      for k in range(2):
        if not self.hidden: #GRAPHIC
          self.teams[k].pli.display()
      return True #a trump was picked
    else :
      return False #nobody picked a trump : it's a white round
      
"""
TESTS 
"""

def test_init():
  myround =  Round(team_names=["Les winners","Les loseurs"],player_names=["Bob","Bill","Fred","John"],player_bots=[True,True,True,True],
                   hidden=False,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]),number=1)


  "check if pioche is empty"

  myround.pli.test("Pli in progress")

  "random draw cards assert that all cards are drawing"
  countinghand=Hand()
  for team in myround.teams :
    for player in team.players :
      assert(len(player.Hand.cards)==player.Hand.rest["cards"]==8)
      countinghand+=player.Hand

  cards_of_pioche=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]

  countinghand.test("Cards",8,8,8,8)

  for i in range(32):
    assert(countinghand.cards[i] not in (countinghand.cards[:i]+countinghand.cards[i+1:])) #check for double
    assert(countinghand.check_card(cards_of_pioche[i]))

  print("test ok")

def test_classic_drawing():

  myround =  Round(team_names=["Les winners","Les loseurs"],player_names=["Bob","Bill","Fred","John"],player_bots=[True,True,True,True],
                   hidden=False,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]),number=1)

  myround.pioche = Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]])
  players=myround.classic_draw()

  "check if pioche is empty"

  myround.pli.test("Pli in progress")

  "check drawing"

  "the order should be"
  "7 8 9 coeur d r 10 pique 7 8 trefle"
  "v d r coeur As pique 7 8 carreau 9 v trefle"
  "10 as coeur 7 pique 9 v d carreau d r trefle"
  "8 9 v pique r 10 as carreau 10 as trefle"
  players_cards=[]
  players_cards.append([Card("7", "coeur"),Card("8", "coeur"),Card("9", "coeur"),
           Card("D", "pique"),Card("R", "pique"),Card("10", "pique"),
           Card("7", "trefle"),Card("8", "trefle")])

  players_cards.append([Card("V", "coeur"),Card("D", "coeur"),Card("R", "coeur"),
           Card("As", "pique"),Card("7", "carreau"),Card("8", "carreau"),
           Card("9", "trefle"),Card("V", "trefle")])

  players_cards.append([Card("10", "coeur"),Card("As", "coeur"),Card("7", "pique"),
           Card("9", "carreau"),Card("V", "carreau"),Card("D", "carreau"),
           Card("D", "trefle"),Card("R", "trefle")])

  players_cards.append([Card("8", "pique"),Card("9", "pique"),Card("V", "pique"),
           Card("R", "carreau"),Card("10", "carreau"),Card("As", "carreau"),
           Card("10", "trefle"),Card("As", "trefle")])

  for p in range(4) :
    myhand=Hand(cards=players[p])
    for i in range(8):
      assert(myhand.check_card(players_cards[p][i]))




def test_cut():

  myround =  Round(team_names=["Les winners","Les loseurs"],player_names=["Bob","Bill","Fred","John"],player_bots=[True,True,True,True],
                   hidden=False,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]),number=1)

  for nb_of_try in range(100):

    myround.pioche = Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]])
    players=myround.classic_draw(cut=True)

    countinghand=Hand(cards= (players[0]+players[1]+players[2]+players[3]) )
    cards_of_pioche=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]

    countinghand.test("Cards",8,8,8,8)


    for i in range(32):
      assert(countinghand.cards[i] not in (countinghand.cards[:i]+countinghand.cards[i+1:])) #check for double
      assert(countinghand.check_card(cards_of_pioche[i]))



def test_getPlayersInOrder():
  myround =  Round(team_names=["Les winners","Les loseurs"],player_names=["Bob","Bill","Fred","John"],player_bots=[True,True,True,True],
                   hidden=False,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]),number=1)

  p=myround.getPlayersInOrder()
  p[1].Hand=Hand(cards=[Card("7","trefle")])
  assert(myround.teams[1].players[0].Hand.check_card(Card("7","trefle")))

  myround =  Round(team_names=["Les winners","Les loseurs"],player_names=["Bob","Bill","Fred","John"],player_bots=[True,True,True,True],
                   hidden=False,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]),number=2)

  p=myround.getPlayersInOrder()
  p[1].Hand=Hand(cards=[Card("7","trefle")])
  assert(myround.teams[0].players[1].Hand.check_card(Card("7","trefle")))

  myround =  Round(team_names=["Les winners","Les loseurs"],player_names=["Bob","Bill","Fred","John"],player_bots=[True,True,True,True],
                   hidden=False,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]),number=7)

  p=myround.getPlayersInOrder()
  p[1].Hand=Hand(cards=[Card("7","trefle")])
  assert(myround.teams[1].players[1].Hand.check_card(Card("7","trefle")))

  myround =  Round(team_names=["Les winners","Les loseurs"],player_names=["Bob","Bill","Fred","John"],player_bots=[True,True,True,True],
                   hidden=False,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]),number=12)

  p=myround.getPlayersInOrder()
  p[1].Hand=Hand(cards=[Card("7","trefle")])
  assert(myround.teams[0].players[0].Hand.check_card(Card("7","trefle")))



def test_choose_trump(): #random test
  myround =  Round(team_names=["Les winners","Les loseurs"],player_names=["Bob","Bill","Fred","John"],player_bots=[True,True,True,True],
                  hidden=False,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]),number=1)
  myround.choose_trump()

def test_cards_update(): #random test
  myround =  Round(team_names=["Les winners","Les loseurs"],player_names=["Bob","Bill","Fred","John"],player_bots=[True,True,True,True],
                   hidden=False,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]),number=1)
  if myround.choose_trump() :
     myround.cards_update()

def test_play_pli(hidden=True): #•fonctionne
  myround =  Round(team_names=["Les winners","Les loseurs"],player_names=["Bob","Bill","Fred","John"],player_bots=[True,True,True,True],
                  hidden=False,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]),number=1)
  if myround.choose_trump() :
    myround.cards_update()
    players=myround.getPlayersInOrder()
    for i in range(8):
      players=myround.play_pli(pli_number=i,players=players)

def test_run():
  for i in range(500):
    myround =  Round(team_names=["Les winners","Les loseurs"],player_names=["Bob","Bill","Fred","John"],player_bots=[True,True,True,True],
                    hidden=True,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]),number=1)
    myround.run()


def test_bot(): #TODO Complete the test
  myround =  Round(team_names=["Les winners","Les loseurs"],player_names=["Bob","Bill","Fred","John"],player_bots=[True,True,True,True],
                  hidden=False,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.NUMBERS for j in const.COLORS[:4]]),number=1)










if __name__=="__main__"   :

  generic.test("init and random draw",test_init)
  generic.test("choose_trump",test_choose_trump)
  generic.test("cards_update",test_cards_update)
  generic.test("play_pli",test_play_pli)
  generic.test("classic_drawing",test_classic_drawing)
  generic.test("cut",test_cut)
  generic.test("getPlayersInOrder",test_getPlayersInOrder)
  generic.test("bot",test_bot)
  generic.test("run",test_run)

