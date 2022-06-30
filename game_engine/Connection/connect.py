import time
import random
import os
from ..Engine import *

class Connect():
    def __init__(self, player, queue, publisher, internCom):
        self.player = player
        self.queue = queue
        self.publisher = publisher
        self.internCom = internCom

    def wait_connection(self):
        count = 0
        print('\nWaiting on other player....')
        while self.publisher.get_subscription_count() != 1:
            time.sleep(1)
        self.publisher.send('READY')
        msg = self.queue.read(wait=True)
        if msg:
            if msg == 'READY':
                print('CONNECTED')
                # FIX FOR KLAS A
                # self.publisher.send('READY')
                return True

    def roll_a_dice(self):
        playerNumber = 0
        targetPlayerNumber = 0
        while playerNumber == targetPlayerNumber:
            playerNumber = random.randint(0,100)
            self.publisher.send(str(playerNumber))
            targetPlayerNumber = int(self.queue.read(wait=True))
            print('You rolled a ' + str(playerNumber) + ' and the other player an ' + str(targetPlayerNumber))
            if playerNumber > targetPlayerNumber:
                print('You begin :)')
                return True
            elif playerNumber < targetPlayerNumber:
                print('The other player begins :(')
                return False
            else:
                print('It\'s a tie, rolling again..')

    def getPos(self):
        if internCOm:
            self.publisher['intern'].send('getPos')
            self.queue.read(wait=True)
            self.publisher['intern'].send('ok')
            coordinate = self.queue.read(wait=True)
            coordinate = coordinate.strip('][').split(',')
            coordinate = Coordinate([int(coordinate[0]),int(coordinate[1])],self.row_size, self.col_size)
            return coordinate
        return False
            



