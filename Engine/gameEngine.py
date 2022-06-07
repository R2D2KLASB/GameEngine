from .player import Player
from .error import *
from .ai import AIPlayer
import os

class GameEngine():
    def __init__(self, row_size, col_size):
        self.row_size = row_size
        self.col_size = col_size

    def setupPlayers(self):
        self.player1 = Player(self.row_size, self.col_size, 'player1')

        self.nextPlayer('player2')

        print('Player 2 Setup Ships')
        self.player2 = AIPlayer(self.row_size, self.col_size, 'player2')


    def playerTurn(self, player, targetPlayer):
        result = False
        # NEED BETTER ERROR HANDLING
        while result is False:
            try:
                result = player.Turn(targetPlayer)
            except Exception as e:
                clear()
                print(e)
                pass
        clear()
        print(player)

    def nextPlayer(self, name=False):
        input('\nNext?')
        clear()
        input((name if name else 'player') + ' ready?')
        clear()

    def play(self):
        while not self.player1.checkDefeated():
            self.nextPlayer(self.player1.name)
            self.playerTurn(self.player1, self.player2)
            if self.player2.checkDefeated():
                break
            self.nextPlayer(self.player2.name)
            self.playerTurn(self.player2, self.player1)
        print(('Player 1' if self.player2.checkDefeated() else 'Player2') + ' WON!')
