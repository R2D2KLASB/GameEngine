from .player import Player
from .error import *


class GameEngine():
    def __init__(self, row_size, col_size):
        self.row_size = row_size
        self.col_size = col_size

    def setupPlayers(self):
        self.player1 = False
        self.player2 = False
        while self.player1 is False:
            try:
                self.player1 = Player(self.row_size, self.col_size, 'player1')
            except Exception as e:
                print(e)
                pass
        self.nextPlayer('player2')
        while self.player2 is False:
            try:
                self.player2 = Player(self.row_size, self.col_size, 'player2')
            except Exception as e:
                clear()
                print(e)
                pass

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
        input('Next?')
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
