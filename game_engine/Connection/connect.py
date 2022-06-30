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
        while self.publisher['extern'].get_subscription_count() != 1:
            time.sleep(1)
        self.publisher['extern'].send('READY')
        msg = self.queue.read(wait=True)
        if msg:
            if msg == 'READY':
                print('CONNECTED')
                # FIX FOR KLAS A
                # self.publisher['extern'].send('READY')
                return True

    def roll_a_dice(self):
        playerNumber = 0
        targetPlayerNumber = 0
        while playerNumber == targetPlayerNumber:
            playerNumber = random.randint(0,100)
            self.publisher['extern'].send(str(playerNumber))
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

    def getPos(self, row_size, col_size):
        if self.internCom:
            self.publisher['intern'].send('getPos')
            self.queue.read(wait=True)
            self.publisher['intern'].send('ok')
            coordinate = self.queue.read(wait=True)
            coordinate = coordinate.strip('][').split(',')
            coordinate = Coordinate([int(coordinate[0]),int(coordinate[1])],row_size, col_size)
            return coordinate
        return False

    def PublishSetup(self, ships):
        shipgcode = [('G6 R%s C%s W%s L%s' % ((ship.coordinates[0].x+1), (ship.coordinates[0].y+1),(1 if ship.orientation else ship.size),(ship.size if ship.orientation else 1))) for ship in ships]
        shipCoordinates = []
        for ship in ships:
            for coordinate in ship.coordinates:
                shipCoordinates += [coordinate.xy]
        self.publisher['intern'].send('boats')
        self.publisher['intern'].send(str(shipCoordinates).replace(' ', ''))
        self.publisher['gcode'].send(('\n'.join(shipgcode))+'\nG28\n')
    
    def sendExtern(self, value):
        self.publisher['extern'].send(value)

    def sendFire(self, coordinate):
        if self.internCom:
            self.publisher['intern'].send('FIRE')
        self.publisher['extern'].send(coordinate.str)
        msg = self.queue.read(wait=True)
        return msg

    def getHit(self, coordinate):
        if self.internCom:
            self.publisher['intern'].send('HIT 0')
            self.publisher['intern'].send('hit')
            self.publisher['intern'].send(str(coordinate.xy + [1]).replace(' ', ''))
            self.publisher['gcode'].send('G4 R%s C%s P0\n' % (coordinate.x+1, coordinate.y+1))

    def getMiss(self, coordinate):
        if self.internCom:
            self.publisher['intern'].send('MISS 0')
            self.publisher['intern'].send('miss')
            self.publisher['intern'].send(str(coordinate.xy + [1]).replace(' ', ''))
            self.publisher['gcode'].send('G5 R%s C%s P0\n' % (coordinate.x+1, coordinate.y+1))

    def getSunk(self, coordinate):
        if self.internCom:
            self.publisher['intern'].send('HIT 0')
            self.publisher['intern'].send('hit')
            self.publisher['intern'].send(str(coordinate.xy + [1]).replace(' ', ''))
            self.publisher['gcode'].send('G4 R%s C%s P0\n' % (coordinate.x+1, coordinate.y+1))
            time.sleep(0.5)
            self.publisher['intern'].send('SUNK 0')

    def getLose(self, coordinate):
        if self.internCom:
            self.publisher['intern'].send('WIN')
            self.publisher['gcode'].send('G8 P1\n')

    def sendHit(self, coordinate):
        if self.internCom:
            self.publisher['intern'].send('HIT 1')
            self.publisher['intern'].send('hit')
            self.publisher['intern'].send(str(coordinate.xy + [0]).replace(' ', ''))
            self.publisher['gcode'].send('G4 R%s C%s P1\n' % (coordinate.x+1, coordinate.y+1))

    def sendMiss(self, coordinate):
        if self.internCom:
            self.publisher['intern'].send('MISS 1')
            self.publisher['intern'].send('miss')
            self.publisher['intern'].send(str(coordinate.xy + [0]).replace(' ', ''))
            self.publisher['gcode'].send('G5 R%s C%s P1\n' % (coordinate.x+1, coordinate.y+1))

    def sendSunk(self, coordinate):
        if self.internCom:
            self.publisher['intern'].send('HIT 1')
            self.publisher['intern'].send('SUNK 1')
            self.publisher['intern'].send('miss')
            self.publisher['intern'].send(str(coordinate.xy + [0]).replace(' ', ''))
            self.publisher['gcode'].send('G4 R%s C%s P1\n' % (coordinate.x+1, coordinate.y+1))

    def sendLose(self):
        if self.internCom:
            self.publisher['intern'].send('LOSE')
            self.publisher['gcode'].send('G8 P0\n')