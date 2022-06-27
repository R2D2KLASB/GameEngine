from .Engine import *
from .Nodes import *
from .Connection import *
import rclpy
import sys
import time
import threading



def play(player, queue, publisher, size):
    clear()

    gameEngine = GameEngine(size)

    player1 = LANPlayer(size[0], size[1], 'Player', publisher, queue) if player == 'console' else AIPlayer(size[0], size[1], 'ai')
    player2 = LANTarget(size[0], size[1], 'target', publisher, queue)


    connection = Connect(player, queue, publisher)
    if connection.wait_connection():
        clear()
        if connection.roll_a_dice():
            gameEngine.setupPlayers(player1, player2)
        else:
            print(player1)
            print('\nWaiting on next move from the other player...')
            gameEngine.setupPlayers(player2, player1)
        gameEngine.play()

    

def main(args=None):
    par = sys.argv

    if len(par) == 3 and (par[-2] == 'console' or par[-2] == 'ai') and (par[-1] == 'A' or par[-1] == 'B'):
        
        player = par[-1]

        rclpy.init()

        queue = Queue()
        
        publisher = Publisher('publisher','game_info/intern/publisher')
        while True:
            publisher.send(input('READY1'))

        extern_publisher = Publisher('extern_publisher', 'game_info/'+('B' if player == 'A' else 'A'))
        extern_listener = Listener('extern_listener', 'game_info/'+player, queue)

        size = [10,10]

        t1 = threading.Thread(target=rclpy.spin, args=(extern_listener,))
        t2 = threading.Thread(target=play, args=(par[-2], queue,extern_publisher, size))

        t1.start()
        t2.start()
    
    else:
        print('Wrong player setup')