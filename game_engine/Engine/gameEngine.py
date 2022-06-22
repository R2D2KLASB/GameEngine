from .player import Player
from .error import *
from .ai import AIPlayer
import os
import time
class GameEngine():
    def __init__(self, row_col_size, player_name, intern_publisher):
        self.row_size = row_col_size[0]
        self.col_size = row_col_size[1]
        self.intern_publisher = intern_publisher
        self.player_name = player_name

    def setupPlayers(self):
        self.player1 = Player(self.row_size, self.col_size, self.intern_publisher, self.player_name)


    def nextPlayer(self, name=False):
        input('\nNext?')
        clear()
        input((name if name else 'player') + ' ready?')
        clear()

    def play(self):
        while not self.player1.checkDefeated():
            if 'ai' not in self.player1.name and 'ai' not in self.player2.name:
                self.nextPlayer(self.player1.name)
            self.player1.Turn(self.player2)
            if self.player2.checkDefeated():
                break
            if 'ai' not in self.player1.name and 'ai' not in self.player2.name:
                self.nextPlayer(self.player2.name)
            self.player2.Turn(self.player1)
        clear()
        print(('Player 1' if self.player2.checkDefeated() else 'Player2') + ' WON!')
        print(self.player1 if self.player2.checkDefeated() else self.player2)

