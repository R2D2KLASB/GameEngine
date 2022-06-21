from .boards import *
from .player import *
import time

import random
class AIPlayer(Player):
    def __init__(self, row_size, col_size, name):
        self.lastMove = 0  # laatste hit: raak etc
        self.hittedMoveStart = None  # coord van geraakte hit
        self.hittedMoveCurrent = None  # hit rondom start hit
        self.possibleMoves = [] # List with al the moves that can be done
        self.aiMoves = []  # moves the AI should do with random
        self.smallestShip = 2 #smallest ship the opponend can still have
        self.enemyShipsAlive = 0 # number of ships killed
        self.currentKilling = [] #when hitting a ship, this keeps track of the killed part
        super().__init__(row_size, col_size, name)

    #Do a move against the other player
    def Attack(self, targetPlayer, coordinate):
        if coordinate not in self.targetBoard.coordinates:
            self.targetBoard.coordinates += [coordinate]
            if targetPlayer.enemyAttack(coordinate): #Hit
                self.targetBoard.updateBoard(coordinate, 'x')
                return 1
            else:                                    #Miss
                self.targetBoard.updateBoard(coordinate, 'o')
                return 0
        return -1                                    #Invalid
        raise ErrorMessage('Target Coordinate already used')


    def setupBoard(self):
        shipSizes = [4, 3, 2]
        while len(shipSizes) > 0:
            result = False
            while result is False:                     #Loop until the boats are placed
                try:
                    orientation = random.randint(0,1)
                    coordinates = []
                    if orientation == 0:
                        x = random.randint(0,(self.row_size-1-shipSizes[0]))
                        y = random.randint(0,self.col_size-1)
                        for i in range(shipSizes[0]):
                            cor = [x,y+i]
                            coordinates+=[Coordinate(cor, self.row_size, self.col_size)]
                    else:
                        x = random.randint(0,self.row_size-1)
                        y = random.randint(0,(self.col_size-1-shipSizes[0]))
                        for i in range(shipSizes[0]):
                            cor = [x+i,y]
                            coordinates+=[Coordinate(cor, self.row_size, self.col_size)]
                    if len(coordinates) in shipSizes:
                        result = self.shipBoard.createShip(coordinates)
                        if result:
                            shipSizes.remove(len(coordinates))
                        clear()
                    
                except Exception as e:
                    clear()
                    pass

        for i in range(self.row_size-1):
            for j in range(self.row_size-1):
                self.possibleMoves.append([i,j])
                self.aiMoves.append([i,j])

    def Turn(self, targetPlayer):

        if self.lastMove == 0:
            cor = self.possibleMoves[random.randint(0, len(self.possibleMoves) - 1)] #random coord
            coordinate = Coordinate(cor, self.row_size, self.col_size)
            self.enemyShipsAlive = targetPlayer.checkAlive()

        #Hitting the rest of the ship
        if self.lastMove == 1:
            x = self.hittedMoveCurrent.x
            y = self.hittedMoveCurrent.y
            if int(x+1) > self.row_size-1:
                self.lastMove = 2
                return self.Turn(targetPlayer)
            else:
                coordinate = Coordinate([x+1, y], self.row_size, self.row_size)

        if self.lastMove == 2:
            x = self.hittedMoveCurrent.x
            y = self.hittedMoveCurrent.y
            if int(x-1) < 0:
                self.lastMove = 3
                return self.Turn(targetPlayer)
            else:
                coordinate = Coordinate([x-1,y], self.row_size, self.row_size)

# bord aflopen, elke hit die mis is kan je [x] vakjes er naast uitsluiten, [x] is hierin het kortste ship van je tegenstander, schuin door t bord heen lopen
#oneven getallen
        if self.lastMove == 3:
            x = self.hittedMoveCurrent.x
            y = self.hittedMoveCurrent.y
            if int(y+1) > self.row_size-1:
                self.lastMove = 4
                return self.Turn(targetPlayer)
            else:
                coordinate = Coordinate([x,y+1], self.row_size, self.row_size)

        if self.lastMove == 4:
            x = self.hittedMoveCurrent.x
            y = self.hittedMoveCurrent.y
            if int(y-1) < 0:
                self.lastMove = 0
                return self.Turn(targetPlayer)
            else:
                coordinate = Coordinate([x,y-1], self.row_size, self.row_size)

        #Check if a coordinate is valid, else retry
        if not [coordinate.x,coordinate.y] in self.possibleMoves:
            if not self.lastMove == 4:
                self.lastMove += 1
                return self.Turn(targetPlayer)
            else:
                self.lastMove = 0
                return self.Turn(targetPlayer)
            return self.Turn(targetPlayer)
        #Do the move
        result = self.Attack(targetPlayer, coordinate)

        #Previous shot was no hit
        if self.lastMove == 0:
            self.hittedMoveStart = coordinate
            self.hittedMoveCurrent = coordinate

            #current shot hitted
            if result == 1:
                self.lastMove = 1
        #Current shot hit
        if result == 1:
            self.hittedMoveCurrent = coordinate
            self.currentKilling.append([coordinate.x, coordinate.y])

            #if the ship is down
            if self.enemyShipsAlive > targetPlayer.checkAlive():
                self.lastMove = 0
                #remove empty coords drom possible coordinates
                for coord in self.currentKilling:
                    if [coord[0] + 1, coord[1]] in self.possibleMoves:
                        self.possibleMoves.remove([coord[0] + 1, coord[1]])
                        if [coord[0] + 1, coord[1]] in self.aiMoves:
                            self.aiMoves.remove([coord[0] + 1, coord[1]])
                    if [coord[0] - 1, coord[1]] in self.possibleMoves:
                        self.possibleMoves.remove([coord[0] - 1, coord[1]])
                        if [coord[0] - 1, coord[1]] in self.aiMoves:
                            self.aiMoves.remove([coord[0] - 1, coord[1]])
                    if [coord[0], coord[1] + 1] in self.possibleMoves:
                        self.possibleMoves.remove([coord[0], coord[1] + 1])
                        if [coord[0], coord[1] + 1] in self.aiMoves:
                            self.aiMoves.remove([coord[0], coord[1] + 1])
                    if [coord[0], coord[1] - 1] in self.possibleMoves:
                        self.possibleMoves.remove([coord[0], coord[1] - 1])
                        if [coord[0], coord[1] - 1] in self.aiMoves:
                            self.aiMoves.remove([coord[0], coord[1] - 1])
                self.currentKilling.clear()
                self.enemyShipsAlive = targetPlayer.checkAlive()
                print("AI killed a ship")
            return

        #Shot was invalid
        if result == -1:
            self.lastMove += 1
            return self.Turn(targetPlayer)
        else:
            #If the coordinate is in possible Coordinates list
            if [coordinate.x,coordinate.y] in self.possibleMoves:
                self.possibleMoves.remove([coordinate.x,coordinate.y]) #Remove from possible coordinates
                self.aiMoves.remove([coordinate.x,coordinate.y])
            else:
                print("Error: coord:" + str(coordinate.x) + ", " + str(coordinate.y) + "not in pos coords") #Error

        #Previous shot hit, ship not down, current shot missed, go to next position to take down ship.
        if result == 0 :
            if self.lastMove > 0:
                self.lastMove += 1
                self.hittedMoveCurrent = self.hittedMoveStart
            if self.lastMove == 0:
                if self.smallestShip > 1:
                    for i in range(self.smallestShip-1):
                        if [coordinate.x - i, coordinate.y] in self.aiMoves:
                            self.aiMoves.remove([coordinate.x - i, coordinate.y])
                        if [coordinate.x + i, coordinate.y] in self.aiMoves:
                            self.aiMoves.remove([coordinate.x + i, coordinate.y])
                        if [coordinate.x, coordinate.y - i] in self.aiMoves:
                            self.aiMoves.remove([coordinate.x, coordinate.y - i])
                        if [coordinate.x, coordinate.y + i] in self.aiMoves:
                            self.aiMoves.remove([coordinate.x, coordinate.y + i])
        return