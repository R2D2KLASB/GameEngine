from .Engine import *
import sys
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def play(player1, player2, size):
    gameEngine = GameEngine(size)

    player1 = Player(size[0], size[1], 'Player1') if player1 == 'console' else AIPlayer(size[0], size[1], 'ai1')
    clear()
    player2 = Player(size[0], size[1], 'Player2') if player2 == 'console' else AIPlayer(size[0], size[1], 'ai2')
    
    gameEngine.setupPlayers(player1, player2)
    gameEngine.play()

def main(args=None):
    par = sys.argv

    if len(par) == 3 and (par[-2] == 'console' or par[-2] == 'ai') and (par[-1] == 'console' or par[-1] == 'ai'):
        play(par[-2], par[-1], [10,10])
    else:
        print('Wrong player setup')