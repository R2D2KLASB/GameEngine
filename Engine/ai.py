from .boards import *
from .player import *
import time

import random
class AIPlayer(Player):
    def __init__(self, row_size, col_size, name):
        super().__init__(row_size, col_size, name)
        self.lastMoves = 0  # laatste hit: raak etc
        self.hittedMoveStart = None  # coord van geraakte hit
        self.hittedMoveCurrent = None  # hit rondom start hit
        self.possibleMoves = [] # List with al the moves that can be done

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

    def Turn(self, targetPlayer):
        result = -1
        if self.lastMoves == 0:
            while result == -1: # Loop until a valid move is done
                try:
                    x = random.randint(0, self.row_size - 1) #random x coord
                    y = random.randint(0, self.col_size - 1) #random y coord
                    cor = [x, y]
                    coordinate = Coordinate(cor, self.row_size, self.col_size)
                    while coordinate in self.targetBoard.coordinates:
                        x = random.randint(0, self.row_size - 1)
                        y = random.randint(0, self.col_size - 1)
                        cor = [x, y]
                        coordinate = Coordinate(cor, self.row_size, self.col_size)
                    result = self.Attack(targetPlayer, coordinate)
                    if result == 1:
                        print(str(x) + ", " + str(y) + "," + str(self.row_size))
                        self.lastMoves = 1
                        self.hittedMoveStart = coordinate
                        self.hittedMoveCurrent = coordinate
                        return
                    if result == 0:
                        return

                except Exception as e:
                    print("FOUT in random")
                    time.sleep(5)
                    pass
                    clear()
            clear()

        #Hitting the rest of the ship
        if self.lastMoves == 1:
            x = self.hittedMoveCurrent.x
            y = self.hittedMoveCurrent.y
            if int(x+1) > self.row_size-1:
                self.lastMoves = 2
                return self.Turn(targetPlayer)
            else:
                coordinate = Coordinate([x+1, y], self.row_size, self.row_size)
                result = self.Attack(targetPlayer, coordinate)
                if result == 1:
                    self.hittedMoveCurrent = coordinate
                    return
                if result == -1:
                    self.lastMoves = 2
                    return self.Turn(targetPlayer)
                if result == 0:
                    self.lastMoves = 2
                    self.hittedMoveCurrent = self.hittedMoveStart
                    return


        if self.lastMoves == 2:
            x = self.hittedMoveCurrent.x
            y = self.hittedMoveCurrent.y
            if int(x-1) < 0:
                self.lastMoves = 3
                return self.Turn(targetPlayer)
            else:
                coordinate = Coordinate([x-1,y], self.row_size, self.row_size)
                result = self.Attack(targetPlayer, coordinate)
                if result == 1:
                    self.hittedMoveCurrent = coordinate
                if result == -1:
                    self.lastMoves = 3
                    return self.Turn(targetPlayer)
                if result == 0:
                    self.lastMoves = 3
                    self.hittedMoveCurrent = self.hittedMoveStart
                return

        if self.lastMoves == 3:
            x = self.hittedMoveCurrent.x
            y = self.hittedMoveCurrent.y
            if int(y+1) > self.row_size-1:
                self.lastMoves = 4
                return self.Turn(targetPlayer)
            else:
                coordinate = Coordinate([x,y+1], self.row_size, self.row_size)
                result = self.Attack(targetPlayer, coordinate)
                if result == 1:
                    self.hittedMoveCurrent = coordinate
                if result == -1:
                    self.lastMoves = 4
                    return self.Turn(targetPlayer)
                if result == 0:
                    self.lastMoves = 4
                    self.hittedMoveCurrent = self.hittedMoveStart
                return

        if self.lastMoves == 4:
            x = self.hittedMoveCurrent.x
            y = self.hittedMoveCurrent.y
            if int(y-1) < 0:
                self.lastMoves = 0
                return self.Turn(targetPlayer)
            else:
                coordinate = Coordinate([x,y-1], self.row_size, self.row_size)
                result = self.Attack(targetPlayer, coordinate)
                if result == 1:
                    self.hittedMoveCurrent = coordinate
                if result == -1:
                    self.lastMoves = 0
                    return self.Turn(targetPlayer)
                if result == 0:
                    self.lastMoves = 0
                    self.hittedMoveCurrent = self.hittedMoveStart
                return