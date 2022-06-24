from .boards import *
from .player import *
import time

import random
class AIPlayer(Player):
    def __init__(self, row_size, col_size, name, optimalisation):
        self.lastMove = 0  # laatste hit: raak etc
        self.hittedMoveStart = None  # coord van geraakte hit
        self.hittedMoveCurrent = None  # hit rondom start hit
        self.possibleMoves = [] # List with al the moves that can be done
        self.aiMoves = []  # moves the AI should do with random
        self.movesDone = [] # shots that the ai tried with random
        self.smallestShip = 2 #smallest ship the opponend can still have
        self.enemyShipsAlive = 0 # number enemy ships alive(needed to check when it kills a new ship)
        self.currentKilling = [] #when hitting a ship, this keeps track of the killed part
        self.optimise = optimalisation # chose a pattern with gaps, lokking at the minimal ship size of opponent
        self.directionKnown = False #When killing a ship, does the AI know the direction of the ship?
        self.horizontal = False #when killing a ship, the ai can skip places where the ship is not by the direction of the ship
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
        shipSizes = [5, 4, 3, 2]
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

        for i in range(self.row_size):
            for j in range(self.row_size):
                self.possibleMoves.append([i,j])
                self.aiMoves.append([i,j])

        random.shuffle(self.aiMoves)
        print("pos mvs: " + str(len(self.possibleMoves)))

    def Turn(self, targetPlayer):
        coordinate = Coordinate([0,0], self.row_size, self.col_size)

        #Preveous shot missed or first shot
        if self.lastMove == 0:
            self.enemyShipsAlive = targetPlayer.checkAlive() #Update the number of living ships from the opponent

            #If shoot optimisation is true, the ai chooses the coords to shoot by looking at the smallest ship of the opponent
            if self.optimise:
                smallest = 10
                for s in targetPlayer.shipBoard.ships: #Update the smallest ship variable
                    if s.size < smallest:
                        smallest = s.size

                if smallest < self.smallestShip:
                    self.smallestShip = smallest
                    for miss in self.movesDone:
                        if self.smallestShip > 1:
                            for i in range(self.smallestShip - 1):
                                if [miss[0] - i, miss[1]] in self.aiMoves:
                                    self.aiMoves.remove([miss[0] - i, miss[1]])
                                if [miss[0] + i, miss[1]] in self.aiMoves:
                                    self.aiMoves.remove([miss[0] + i, miss[1]])
                                if [miss[0], miss[1] - i] in self.aiMoves:
                                    self.aiMoves.remove([miss[0], miss[1] - i])
                                if [miss[0], miss[1] + i] in self.aiMoves:
                                    self.aiMoves.remove([miss[0], miss[1] + i])

                # If the AI has smart moves in its list:
                if len(self.aiMoves) > 0:
                    cor = self.aiMoves[random.randint(0, len(self.aiMoves) - 1)] #random coord from the smart moves
                else:
                    print("No smart moves!") #//TODO code maken om alle dubbele gaten in AI moves te gooien, 2 schip leeft alleen nog
                    cor = self.possibleMoves[random.randint(0, len(self.possibleMoves) - 1)] #random coord from the possible coords list
            else:
                cor = self.possibleMoves[random.randint(0, len(self.possibleMoves) - 1)]  # random coord from the possible coords list
            coordinate = Coordinate(cor, self.row_size, self.col_size)

        #Hitting the rest of the enemy ship
        if self.lastMove == 1:
            if self.directionKnown and self.horizontal == False:
                self.lastMove == 3
                return self.Turn(targetPlayer)

            x = self.hittedMoveCurrent.x
            y = self.hittedMoveCurrent.y
            if int(x+1) > self.row_size-1:
                self.lastMove = 2
                self.hittedMoveCurrent = self.hittedMoveStart
                return self.Turn(targetPlayer)
            else:
                coordinate = Coordinate([x+1, y], self.row_size, self.row_size)

        if self.lastMove == 2:
            if self.directionKnown and self.horizontal == False:
                self.lastMove == 3
                return self.Turn(targetPlayer)

            x = self.hittedMoveCurrent.x
            y = self.hittedMoveCurrent.y
            if int(x-1) < 0:
                self.lastMove = 3
                self.hittedMoveCurrent = self.hittedMoveStart
                return self.Turn(targetPlayer)
            else:
                coordinate = Coordinate([x-1,y], self.row_size, self.row_size)

        if self.lastMove == 3:
            if self.directionKnown and self.horizontal:
                self.lastMove == 1
                return self.Turn(targetPlayer) #TODO recursive error

            x = self.hittedMoveCurrent.x
            y = self.hittedMoveCurrent.y
            if int(y+1) > self.row_size-1:
                self.lastMove = 4
                self.hittedMoveCurrent = self.hittedMoveStart
                return self.Turn(targetPlayer)
            else:
                coordinate = Coordinate([x,y+1], self.row_size, self.row_size)

        if self.lastMove == 4:
            if self.directionKnown and self.horizontal == True:
                self.lastMove == 1
                return self.Turn(targetPlayer)

            x = self.hittedMoveCurrent.x
            y = self.hittedMoveCurrent.y
            if int(y-1) < 0:
                self.lastMove = 3
                self.hittedMoveCurrent = self.hittedMoveStart
                return self.Turn(targetPlayer)
            else:
                coordinate = Coordinate([x,y-1], self.row_size, self.row_size)

        #Check if a coordinate is valid, else retry
        if not [coordinate.x,coordinate.y] in self.possibleMoves:
            if self.lastMove < 5:
                if self.lastMove < 4 and self.lastMove > 0:
                    self.lastMove += 1
                    self.hittedMoveCurrent = self.hittedMoveStart
                    return self.Turn(targetPlayer)
                else:
                    self.lastMove = 0
                    # self.directionKnown = False
                    return self.Turn(targetPlayer)
            else:
                self.lastMove = 0
                return self.Turn(targetPlayer)

        #Do the move
        result = self.Attack(targetPlayer, coordinate)


        print(self.name + " Result: " + str(result) + " ; " + str(coordinate.xy) + ", "+ str(self.directionKnown) + ", " + str(self.horizontal)+ "lm: " + str(self.lastMove))


        #Previous shot was random
        if self.lastMove == 0:
            self.hittedMoveCurrent = coordinate

            #current shot hitted
            if result == 1:
                self.hittedMoveStart = coordinate
                self.lastMove = 1

                #If shoot optimisation is True, the ai checks if the ship can be horizontal, looking at minimal ship size needed
                if self.optimise:
                    maxShipSizeH = 0
                    maxShipSizeV = 0
                    for i in range(self.row_size-1):
                        if [coordinate.x - i, coordinate.y] in self.possibleMoves:
                            maxShipSizeH += 1
                        else:
                            break
                    for i in range(self.row_size-1):
                        if [coordinate.x + i, coordinate.y] in self.possibleMoves:
                            maxShipSizeH += 1
                        else:
                            break
                    for i in range(self.row_size-1):
                        if [coordinate.x, coordinate.y - i] in self.possibleMoves:
                            maxShipSizeV += 1
                        else:
                            break
                    for i in range(self.row_size-1):
                        if [coordinate.x, coordinate.y + i] in self.possibleMoves:
                            maxShipSizeV += 1
                        else:
                            break

                    #If a horizontal ship doesnt fit it must be vertical
                    if maxShipSizeH < self.smallestShip:
                        self.horizontal = False
                        print("vertical1: " + str(coordinate.xy))
                        self.directionKnown = True

                    #If a vertical ship doesnt fit, it must be horizontal
                    if maxShipSizeV < self.smallestShip:
                        print("horizontal1: " + str(coordinate.xy))
                        self.horizontal = True
                        self.directionKnown = True

        #Current shot hitted
        if result == 1:
            self.hittedMoveCurrent = coordinate
            self.currentKilling.append([coordinate.x, coordinate.y])

            #if the ship is down
            if self.enemyShipsAlive > targetPlayer.checkAlive():

                #remove empty coords around the killed ship from possible coordinates
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
                self.directionKnown = False
                self.enemyShipsAlive -= 1
                self.lastMove = 0
                print(self.name + " killed a ship " + str(coordinate.x) + " : " + str(coordinate.y))

            if len(self.currentKilling) == 2:
                if self.optimise:
                    self.directionKnown = True
                    # if coordinate x1 == x2 (Vertical)
                    if self.currentKilling[0][0] == self.currentKilling[1][0]:
                        print("vertical: " + str(coordinate.xy))
                        self.horizontal = False
                    elif self.currentKilling[0][1] == self.currentKilling[1][1]:
                        print("horizontal: " + str(coordinate.xy))
                        self.horizontal = True

        #Shot was invalid, retry
        if result == -1:
            self.lastMove = 0
            print(self)
            return self.Turn(targetPlayer)
        else:
            self.movesDone.append([coordinate.x, coordinate.y])

            # if shoot optimisation is True, remove empty location from shoot list
            if self.optimise:
                if self.smallestShip > 1:
                    for i in range(1, self.smallestShip):
                        if [coordinate.x - i, coordinate.y] in self.aiMoves:
                            self.aiMoves.remove([coordinate.x - i, coordinate.y])
                        if [coordinate.x + i, coordinate.y] in self.aiMoves:
                            self.aiMoves.remove([coordinate.x + i, coordinate.y])
                        if [coordinate.x, coordinate.y - i] in self.aiMoves:
                            self.aiMoves.remove([coordinate.x, coordinate.y - i])
                        if [coordinate.x, coordinate.y + i] in self.aiMoves:
                            self.aiMoves.remove([coordinate.x, coordinate.y + i])


            #If the coordinate is in the possible Coordinates list
            if [coordinate.x,coordinate.y] in self.possibleMoves:
                self.possibleMoves.remove([coordinate.x,coordinate.y])  #Remove from possibleMoves

                #If the coordinate is in the aiMoves list
                if [coordinate.x,coordinate.y] in self.aiMoves:
                    self.aiMoves.remove([coordinate.x,coordinate.y])    #Remove from aiMoves
            else:
                print("Error: coord:" + str(coordinate.x) + ", " + str(coordinate.y) + "not in pos coords") #Error

        #missed
        if result == 0 :
            # Previous shot hitted, ship not down, current shot missed, go to next position to take down the rest of the ship.
            if self.lastMove > 0:
                self.lastMove += 1
                self.hittedMoveCurrent = self.hittedMoveStart
        return