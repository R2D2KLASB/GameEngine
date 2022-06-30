from .Engine import *
from .Nodes import *
from .Connection import *
from .Camera import *
import rclpy
import sys
import time
import threading


def play(player, queue, publisher, size, ros, camera=False):
    clear()
    time.sleep(2)
    publisher['intern'].send('READY')
    # publisher['gcode'].send('G3\n')

    if camera:
        if ros:
            camera = ShipDetection(queue, publisher)
        else:
            camera = ShipDetection()

    player1 = LANPlayer(size[0], size[1], 'Player', publisher, queue, camera) if player == 'console' else AIPlayer(size[0], size[1], 'ai')
    
    player2 = LANTarget(size[0], size[1], 'target', publisher, queue)

    gameEngine = GameEngine(size)

    connection = Connect(player, queue, publisher['extern'])
    if connection.wait_connection():
        clear()
        if connection.roll_a_dice():
            gameEngine.setupPlayers(player1, player2)
        else:
            print(player1)
            gameEngine.setupPlayers(player2, player1)
        gameEngine.play()

    

def main(args=None):
    par = sys.argv

    if len(par) == 3 and (par[-2] == 'console' or par[-2] == 'ai') and (par[-1] == 'A' or par[-1] == 'B'):
        
        player = par[-1]

        rclpy.init()

        extern_queue = Queue()

        size = [10,10]

        publisher = {}
        listener = {}

        publisher['extern'] = Publisher('extern_publisher', 'game_info/'+('B' if player == 'A' else 'A'))
        listener['extern'] = Listener('extern_listener', 'game_info/'+player, extern_queue)

        ros = False

        if par[-1] == 'B':
            camera = False
            if ros:
                publisher['intern'] = Publisher('intern_publisher', 'game_info/intern/publish')
                publisher['gcode'] = Publisher('gcode_publisher', 'game_info/intern/gcode')
            else:
                publisher['intern'] = Publisher('intern_publisher', 'game_info/intern/publish_test')
                publisher['gcode'] = Publisher('gcode_publisher', 'game_info/intern/gcode_test')

        elif par[-1] == 'A':
            publisher['intern'] = Publisher('intern_publisher', 'game_info/intern/test_publish')
            publisher['gcode'] = Publisher('gcode_publisher', 'game_info/intern/test_gcode')
            camera = False

        t1 = threading.Thread(target=rclpy.spin, args=(listener['extern'],))
        t2 = threading.Thread(target=play, args=(par[-2], extern_queue, publisher, size,ros, camera))

    
        t1.start()
        t2.start()
    
    else:
        print('Wrong player setup')