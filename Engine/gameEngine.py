from .player import Player
from .error import *
from .ai import AIPlayer
import os

class GameEngine():
    def __init__(self, row_size, col_size):
        self.row_size = row_size
        self.col_size = col_size

    def setupPlayers(self):
        self.player1 = Player(self.row_size, self.col_size, 'Merry')

        # if 'ai' not in self.player1.name and 'ai' not in self.player2.name:
        #     self.nextPlayer('player2')

        self.player2 = AIPlayer(self.row_size, self.col_size, 'ai', True)

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
        print((self.player1.name if self.player2.checkDefeated() else self.player2.name) + ' WON!')
        print(self.player1 if self.player2.checkDefeated() else self.player2)

