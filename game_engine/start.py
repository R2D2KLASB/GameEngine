from .Engine import GameEngine
from .Nodes import *
import rclpy
import time


def main(args=None):
    rclpy.init(args=args)

    intern_publisher = InternPublisher()

    gameEngine = GameEngine([6,6], intern_publisher)
    gameEngine.setupPlayers()
    gameEngine.play()




if __name__ == '__main__':
    main()