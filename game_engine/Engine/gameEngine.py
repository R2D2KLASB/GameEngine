from .error import *
import os
import time
class GameEngine():
    # initializes the game engine given the row and column sizes
    def __init__(self, row_col_size):
        self.row_size = row_col_size[0]
        self.col_size = row_col_size[1]

    # sets the players up
    def setupPlayers(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    # it will print the next
    # it will print the name of the player if a name is given, else it will print player with 'ready?' behind 
    def nextPlayer(self, name=False):
        input('\nNext?')
        clear()
        input((name if name else 'player') + ' ready?')
        clear()

    # starts the game and plays until one of 2 players have won
    def play(self):
        while not self.player1.checkDefeated():
            if ('ai' not in self.player1.name and 'ai' not in self.player2.name) and ('target' not in self.player1.name and 'target' not in self.player2.name):
                self.nextPlayer(self.player1.name)
            self.player1.Turn(self.player2)
            if self.player2.checkDefeated():
                break
            if ('ai' not in self.player1.name and 'ai' not in self.player2.name) and ('target' not in self.player1.name and 'target' not in self.player2.name):
                self.nextPlayer(self.player2.name)
            self.player2.Turn(self.player1)
        clear()
        print((self.player1.name if self.player2.checkDefeated() else self.player2.name) + ' WON!')
        print(self.player1 if self.player2.checkDefeated() else self.player2)

