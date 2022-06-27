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
        self.coordinate = None
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
        raise ErrorMessage('Target self.Coordinate already used')

    #Setup the ship board using random places to place a ship
    def setupBoard(self):
        shipSizes = [5, 4, 3, 3, 2]
        while len(shipSizes) > 0:
            result = False
            while result is False:                     #Loop until the boats are placed
                try:
                    orientation = random.randint(0,1)
                    self.coordinates = []
                    if orientation == 0:
                        x = random.randint(0,(self.row_size-1-shipSizes[0]))
                        y = random.randint(0,self.col_size-1)
                        for i in range(shipSizes[0]):
                            cor = [x,y+i]
                            self.coordinates+=[Coordinate(cor, self.row_size, self.col_size)]
                    else:
                        x = random.randint(0,self.row_size-1)
                        y = random.randint(0,(self.col_size-1-shipSizes[0]))
                        for i in range(shipSizes[0]):
                            cor = [x+i,y]
                            self.coordinates+=[Coordinate(cor, self.row_size, self.col_size)]
                    if len(self.coordinates) in shipSizes:
                        result = self.shipBoard.createShip(self.coordinates)
                        if result:
                            shipSizes.remove(len(self.coordinates))
                        clear()
                    
                except Exception as e:
                    clear()
                    pass

        for i in range(self.row_size):
            for j in range(self.row_size):
                self.possibleMoves.append([i,j])
                self.aiMoves.append([i,j])

        random.shuffle(self.aiMoves)

    #TODO na hit, random keuze waar start met schip killen

    #Update the list of smart moves for the AI, used after killing the smallest ship of the opponent,
    #Only used if optomise boolean is True
    def UpdateAIMoves(self, isEmpty):
        if isEmpty:
            for i in range(0, self.row_size-2):
                for j in range(0, self.row_size - 2):
                    if [i,j] in self.possibleMoves and [i+1, j] in self.possibleMoves:
                        if [i,j] not in self.aiMoves:
                            self.aiMoves.append([i,j])
                        if [i+1,j] not in self.aiMoves:
                            self.aiMoves.append([i+1, j])
                    if [i,j] in self.possibleMoves and [i, j+1] in self.possibleMoves:
                        if [i,j] not in self.aiMoves:
                            self.aiMoves.append([i,j])
                        if [i,j+1] not in self.aiMoves:
                            self.aiMoves.append([i, j+1])
        else:
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

    #Get a random location from the moves list and do a move
    #also updates some local variables
    def RandomMove(self, targetPlayer):
        self.enemyShipsAlive = targetPlayer.checkAlive()  # Update the number of living ships from the opponent

        # If shoot optimisation is true, the ai chooses the coords to shoot by looking at the smallest ship of the opponent
        if self.optimise:
            smallest = 10
            for s in targetPlayer.shipBoard.ships:  # Update the smallest ship variable
                if s.size < smallest:
                    smallest = s.size

            if smallest < self.smallestShip:
                self.smallestShip = smallest
                self.UpdateAIMoves(False)  # add the smartest moves at this moment to the AImoves list

            # If the AI has smart moves in its list:
            if len(self.aiMoves) > 0:
                cor = self.aiMoves[random.randint(0, len(self.aiMoves) - 1)]  # random coord from the smart moves
            else:
                self.UpdateAIMoves(True)
                cor = self.possibleMoves[
                    random.randint(0, len(self.possibleMoves) - 1)]  # random coord from the possible coords list
        else:
            cor = self.possibleMoves[
                random.randint(0, len(self.possibleMoves) - 1)]  # random coord from the possible coords list
        self.coordinate = Coordinate(cor, self.row_size, self.col_size)

    #if ship is found, Horizontally sink the rest of the ship, going Right
    def MoveXupper(self, targetPlayer):
        if self.directionKnown and self.horizontal == False:
            self.lastMove == 3
            return 0

        x = self.hittedMoveCurrent.x
        y = self.hittedMoveCurrent.y
        if int(x + 1) > self.row_size - 1:
            self.lastMove = 2
            self.hittedMoveCurrent = self.hittedMoveStart
            return 0
        else:
            self.coordinate = Coordinate([x + 1, y], self.row_size, self.row_size)
        return 1

    #if ship is found, Horizontally sink the rest of the ship, going Left
    def MoveXlower(self, targetPlayer):
        if self.directionKnown and self.horizontal == False:
            self.lastMove == 3
            return 0

        x = self.hittedMoveCurrent.x
        y = self.hittedMoveCurrent.y
        if int(x - 1) < 0:
            self.lastMove = 3
            self.hittedMoveCurrent = self.hittedMoveStart
            return 0
        else:
            self.coordinate = Coordinate([x - 1, y], self.row_size, self.row_size)
        return 1

    #If a ship is found, sinking the rest of the ship vertically, going Down
    def MoveYupper(self, targetPlayer):
        if self.directionKnown and self.horizontal:
            self.lastMove == 1
            return 0

        x = self.hittedMoveCurrent.x
        y = self.hittedMoveCurrent.y
        if int(y + 1) > self.row_size - 1:
            self.lastMove = 4
            self.hittedMoveCurrent = self.hittedMoveStart
            return 0
        else:
            self.coordinate = Coordinate([x, y + 1], self.row_size, self.row_size)
        return 1

    #If a ship is found, sinking the rest of the ship vertically, going Up
    def MoveYlower(self, targetPlayer):
        if self.directionKnown and self.horizontal == True:
            self.lastMove == 1
            return 0

        x = self.hittedMoveCurrent.x
        y = self.hittedMoveCurrent.y
        if int(y - 1) < 0:
            self.lastMove = 3
            self.hittedMoveCurrent = self.hittedMoveStart
            return 0
        else:
            self.coordinate = Coordinate([x, y - 1], self.row_size, self.row_size)
        return 1

    #Checks if the next chosen coordinate is valid, if not, choses wich function is best to find a new coordinate
    def CheckCoord(self, targetPlayer):
        if not [self.coordinate.x,self.coordinate.y] in self.possibleMoves:
            if self.lastMove < 5:
                if self.lastMove < 4 and self.lastMove > 0:
                    self.lastMove += 1
                    self.hittedMoveCurrent = self.hittedMoveStart
                    return 0
                else:
                    self.lastMove = 0
                    return 0
            else:
                self.lastMove = 0
                return 0
        return 1

    #Function called when the previous hit was a random coordinate, and the current shot hitted too
    def PreviousRandom_CurrentHit(self):
        self.hittedMoveStart = self.coordinate
        self.lastMove = 1

        # If shoot optimisation is True, the ai checks if the ship can be horizontal, looking at minimal ship size needed
        if self.optimise:
            maxShipSizeH = 0
            maxShipSizeV = 0
            for i in range(self.row_size - 1):
                if [self.coordinate.x - i, self.coordinate.y] in self.possibleMoves:
                    maxShipSizeH += 1
                else:
                    break
            for i in range(self.row_size - 1):
                if [self.coordinate.x + i, self.coordinate.y] in self.possibleMoves:
                    maxShipSizeH += 1
                else:
                    break
            for i in range(self.row_size - 1):
                if [self.coordinate.x, self.coordinate.y - i] in self.possibleMoves:
                    maxShipSizeV += 1
                else:
                    break
            for i in range(self.row_size - 1):
                if [self.coordinate.x, self.coordinate.y + i] in self.possibleMoves:
                    maxShipSizeV += 1
                else:
                    break

            # If a horizontal ship doesnt fit it must be vertical
            if maxShipSizeH < self.smallestShip:
                self.horizontal = False
                print("vertical1: " + str(self.coordinate.xy))
                self.directionKnown = True

            # If a vertical ship doesnt fit, it must be horizontal
            if maxShipSizeV < self.smallestShip:
                print("horizontal1: " + str(self.coordinate.xy))
                self.horizontal = True
                self.directionKnown = True

    #If a shot was hit:
    def ShotHit(self, targetPlayer):
        self.hittedMoveCurrent = self.coordinate
        self.currentKilling.append([self.coordinate.x, self.coordinate.y])

        # if the ship is down
        if self.enemyShipsAlive > targetPlayer.checkAlive():
            # remove empty coords around the killed ship from possible self.coordinates
            self.ShipKilledUpdateMoves()

        if len(self.currentKilling) == 2:
            if self.optimise:
                self.directionKnown = True
                # if self.coordinate x1 == x2 (Vertical)
                if self.currentKilling[0][0] == self.currentKilling[1][0]:
                    print("vertical: " + str(self.coordinate.xy))
                    self.horizontal = False
                elif self.currentKilling[0][1] == self.currentKilling[1][1]:
                    print("horizontal: " + str(self.coordinate.xy))
                    self.horizontal = True

    #Removes the move from possible moves, if opomisation is True, it removes every useless move from possible moves list
    def UpdateMovesList(self):
        self.movesDone.append([self.coordinate.x, self.coordinate.y])

        # if shoot optimisation is True, remove empty location from shoot list
        if self.optimise:
            if self.smallestShip > 1:
                for i in range(1, self.smallestShip):
                    if [self.coordinate.x - i, self.coordinate.y] in self.aiMoves:
                        self.aiMoves.remove([self.coordinate.x - i, self.coordinate.y])
                    if [self.coordinate.x + i, self.coordinate.y] in self.aiMoves:
                        self.aiMoves.remove([self.coordinate.x + i, self.coordinate.y])
                    if [self.coordinate.x, self.coordinate.y - i] in self.aiMoves:
                        self.aiMoves.remove([self.coordinate.x, self.coordinate.y - i])
                    if [self.coordinate.x, self.coordinate.y + i] in self.aiMoves:
                        self.aiMoves.remove([self.coordinate.x, self.coordinate.y + i])

        # If the self.coordinate is in the possible self.Coordinates list
        if [self.coordinate.x, self.coordinate.y] in self.possibleMoves:
            self.possibleMoves.remove([self.coordinate.x, self.coordinate.y])  # Remove from possibleMoves

            # If the self.coordinate is in the aiMoves list
            if [self.coordinate.x, self.coordinate.y] in self.aiMoves:
                self.aiMoves.remove([self.coordinate.x, self.coordinate.y])  # Remove from aiMoves

    #After a ship is sunk, removes all empty coordinates
    def ShipKilledUpdateMoves(self):
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
        print(self.name + " killed a ship " + str(self.coordinate.x) + " : " + str(self.coordinate.y))

    #Its the AI's turn to play
    def Turn(self, targetPlayer):
        self.coordinate = Coordinate([0,0], self.row_size, self.col_size)

        #Preveous shot missed or first shot
        if self.lastMove == 0:
            if (self.RandomMove(targetPlayer)) == 0:
                return self.Turn(targetPlayer)

        #Hitting the rest of the enemy ship
        if self.lastMove == 1:
            if self.MoveXupper(targetPlayer) == 0:
                return self.Turn(targetPlayer)

        elif self.lastMove == 2:
            if self.MoveXlower(targetPlayer) == 0:
                return self.Turn(targetPlayer)

        elif self.lastMove == 3:
            if self.MoveYupper(targetPlayer) == 0:
                return self.Turn(targetPlayer)

        elif self.lastMove == 4:
            if self.MoveYlower(targetPlayer) == 0:
                return self.Turn(targetPlayer)

        #Check if a self.coordinate is valid, else retry
        if self.CheckCoord(targetPlayer) == 0:
            return self.Turn(targetPlayer)

        #Do the move
        result = self.Attack(targetPlayer, self.coordinate)
        print(self.name + " Result: " + str(result) + " ; " + str(self.coordinate.xy) + ", "+ str(self.directionKnown) + ", " + str(self.horizontal)+ "lm: " + str(self.lastMove))

        #Previous shot was random
        if self.lastMove == 0:
            self.hittedMoveCurrent = self.coordinate

            #current shot hitted
            if result == 1:
                self.PreviousRandom_CurrentHit()

        #Shot hitted
        if result == 1:
            if self.ShotHit(targetPlayer) == 0:
                return self.Turn(targetPlayer)

        #Shot was invalid, retry
        if result == -1:
            self.lastMove = 0
            print(self)
            return self.Turn(targetPlayer)

        #Shot valid
        else:
            self.UpdateMovesList()

        #missed
        if result == 0 :
            # Previous shot hitted, ship not down, current shot missed, go to next position to take down the rest of the ship.
            if self.lastMove > 0:
                if self.lastMove < 4:
                    self.lastMove += 1
                    self.hittedMoveCurrent = self.hittedMoveStart
        return