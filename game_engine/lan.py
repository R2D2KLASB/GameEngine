from .Engine import GameEngine
from .Engine import Player
from .Nodes import *
from .Connection import *
import rclpy
import sys
import time
import threading



def play(player, queue, publisher):
    # gameEngine = GameEngine([6,6], player, publisher)
    # gameEngine.setupPlayers()
    connection = Connect(player, queue, publisher)
    if connection.wait_connection():
        print(connection.roll_a_dice())

    

def main(args=None):
    par = sys.argv

    if len(par) == 2 and ( par[-1] == 'A' or par[-1] == 'B'):
        
        player = par[-1]

        rclpy.init()

        queue = Queue()

        extern_publisher = Publisher('extern_publisher', 'game_info/'+('B' if player == 'A' else 'A'))
        extern_listener = Listener('extern_listener', 'game_info/'+player, queue)

        t1 = threading.Thread(target=rclpy.spin, args=(extern_listener,))
        t2 = threading.Thread(target=play, args=(player,queue,extern_publisher))

        t1.start()
        t2.start()
    
    else:
        print('No player para')