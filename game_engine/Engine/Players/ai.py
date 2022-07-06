from ..boards import *
from .player import Player

import random
class AIPlayer(Player):
    def __init__(self, row_size, col_size, name, optimalisation=True):
        self.lastMove = 0  # Last tried method for picking a coord
        self.movesTried = [] # Moves tried, killing a found ship
        self.move = False # Move is done
        self.hittedMoveStart = None  # Coord of first hit shot(of 1 ship)
        self.hittedMoveCurrent = None  # Last tried hit, sinking a ship
        self.possibleMoves = [] # List with al the moves that can be done
        self.aiMoves = []  # Moves the AI should do with random
        self.movesDone = [] # Shots that the ai tried with random
        self.smallestShip = 2 # Smallest ship the opponend can still have
        self.enemyShipsAlive = 0 # Number enemy ships alive(needed to check when it kills a new ship)
        self.currentKilling = [] # When hitting a ship, this keeps track of the killed part
        self.optimise = optimalisation # Chose a pattern with gaps, lokking at the minimal ship size of opponent
        self.directionKnown = False # When killing a ship, does the AI know the direction of the ship?
        self.horizontal = False # When killing a ship, the ai can skip places where the ship is not by the direction of the ship
        self.coordinate = None # The current coordinate
        self.enemyShips = [5,4,3,3,2] # List of enemy ships, to keep track wich ships are still alive
        super().__init__(row_size, col_size, name)

    #Do a move against the other player
    def Attack(self, targetPlayer, coordinate):
        if coordinate not in self.targetBoard.coordinates:
            self.targetBoard.coordinates += [coordinate]
            result = targetPlayer.enemyAttack(coordinate)
            if result == 'HIT':
                self.targetBoard.updateBoard(coordinate, 'x')
                return 1
            elif result == 'MISS':
                self.targetBoard.updateBoard(coordinate, 'o')
                return 0
            elif result == 'SUNK':
                self.targetBoard.updateBoard(coordinate, 'x')
                self.targetDefeated += 1
                return 1
            elif result == 'LOSE':
                self.targetBoard.updateBoard(coordinate, 'x')
                self.targetDefeated += 1
                return 1
        return -1
        raise ErrorMessage('Target Coordinate already used')

    # Create the AI's ship board
    def setupBoard(self):
        shipSizes = self.shipSizes
        while len(shipSizes) > 0:
            result = False
            while result is False:
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

        #Creating 2 lists with all possible moves and shuffle them
        for i in range(self.row_size):
            for j in range(self.row_size):
                self.possibleMoves.append([i,j])
                self.aiMoves.append([i,j])
        random.shuffle(self.aiMoves)
            

    # After every move, this function chooses the next function to pick a coord
    def NextMove(self, first, i):
        # First
        if first == True:
            move = random.randint(1, 5)
            self.lastMove = move
            self.movesTried.append(move)
        else:
            self.hittedMoveCurrent = self.hittedMoveStart
            if self.directionKnown:
                if self.horizontal:
                    if self.lastMove == 1:
                        self.lastMove = 2
                        return
                    if self.lastMove == 2:
                        self.lastMove = 1
                        return
                    else:
                        self.lastMove = 1
                        return
                else:
                    if self.lastMove == 3:
                        self.lastMove = 4
                        return
                    if self.lastMove == 4:
                        self.lastMove = 3
                        return
                    else:
                        self.lastMove = 3
                        return
            else:
                if self.lastMove < 5:
                    move = self.lastMove +1
                else:
                    move = 1
                if move in self.movesTried:
                    i += 1
                    if i < 10:
                        self.lastMove = move
                        return self.NextMove(False, i)
                    else:
                        self.lastMove = 0
                        return
                else:
                    self.lastMove = move
                    self.movesTried.append(move)
                    return


    #Update the list of smart moves for the AI, used after killing the smallest ship of the opponent,
    #Only used if optomise boolean is True
    def UpdateAIMoves(self, isEmpty):
        #The ai has no more smart moves, filling smart moves
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

        #The smallest ship of the opponent is sunk
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

        # If shoot optimisation is true, the ai uses moves from the smart moves list
        if self.optimise:

            # Update the smallest ship variable
            smallest = 10
            for s in self.enemyShips:
                if s < smallest:
                    smallest = s

            if smallest > self.smallestShip:
                self.smallestShip = smallest
                self.UpdateAIMoves(False)  # Remove moves that are not smart anymore

            # If the AI has smart moves in its list:
            if len(self.aiMoves) > 0:
                cor = self.aiMoves[random.randint(0, len(self.aiMoves) - 1)]  # random coord from the smart moves
            else:
                self.UpdateAIMoves(True)    # Update smart moves list
                cor = self.possibleMoves[random.randint(0, len(self.possibleMoves) - 1)] # Get a random coordinate from the possible moves list
        else:
            cor = self.possibleMoves[random.randint(0, len(self.possibleMoves) - 1)]
        self.coordinate = Coordinate(cor, self.row_size, self.col_size)
        self.move = True

    # If ship is found, Horizontally sink the rest of the ship, going Right
    def MoveXupper(self, targetPlayer):
        x = self.hittedMoveCurrent.x
        y = self.hittedMoveCurrent.y
        self.move = True
        if int(x + 1) > self.row_size - 1:
            return 0
        else:
            self.coordinate = Coordinate([x + 1, y], self.row_size, self.row_size)
        return 1

    # If ship is found, Horizontally sink the rest of the ship, going Left
    def MoveXlower(self, targetPlayer):
        x = self.hittedMoveCurrent.x
        y = self.hittedMoveCurrent.y
        self.move = True
        if int(x - 1) < 0:
            return 0
        else:
            self.coordinate = Coordinate([x - 1, y], self.row_size, self.row_size)
        return 1

    # If a ship is found, sinking the rest of the ship vertically, going Down
    def MoveYupper(self, targetPlayer):
        x = self.hittedMoveCurrent.x
        y = self.hittedMoveCurrent.y
        self.move = True
        if int(y + 1) > self.row_size - 1:
            return 0
        else:
            self.coordinate = Coordinate([x, y + 1], self.row_size, self.row_size)
        return 1

    # If a ship is found, sinking the rest of the ship vertically, going Up
    def MoveYlower(self, targetPlayer):
        x = self.hittedMoveCurrent.x
        y = self.hittedMoveCurrent.y
        self.move = True
        if int(y - 1) < 0:
            return 0
        else:
            self.coordinate = Coordinate([x, y - 1], self.row_size, self.row_size)
        return 1

    # Checks if the next chosen coordinate is valid, if not, choses wich function is best to find a new coordinate
    def CheckCoord(self, targetPlayer):
        if not [self.coordinate.x,self.coordinate.y] in self.possibleMoves:
            if self.lastMove > 0:
                self.NextMove(False, 0)
            return 0
        return 1

    # Function called when the previous hit was a random coordinate and the current shot hitted
    def PreviousRandom_CurrentHit(self):
        self.hittedMoveStart = self.coordinate
        self.NextMove(True, 0)

        # If shoot optimisation is True, the ai checks if the ship can be horizontal, looking at minimal ship size needed
        if self.optimise:
            maxShipSizeH = 0
            maxShipSizeV = 0
            for i in range(1, self.row_size - 1):
                if [self.coordinate.x - i, self.coordinate.y] in self.possibleMoves:
                    maxShipSizeH += 1
                else:
                    break
            for i in range(1, self.row_size - 1):
                if [self.coordinate.x + i, self.coordinate.y] in self.possibleMoves:
                    maxShipSizeH += 1
                else:
                    break
            for i in range(1, self.row_size - 1):
                if [self.coordinate.x, self.coordinate.y - i] in self.possibleMoves:
                    maxShipSizeV += 1
                else:
                    break
            for i in range(1, self.row_size - 1):
                if [self.coordinate.x, self.coordinate.y + i] in self.possibleMoves:
                    maxShipSizeV += 1
                else:
                    break

            # If a horizontal ship doesnt fit it must be vertical
            if maxShipSizeH < self.smallestShip-1 and maxShipSizeV >= self.smallestShip-1:
                self.horizontal = False
                self.directionKnown = True

            # If a vertical ship doesnt fit, it must be horizontal
            if maxShipSizeV < self.smallestShip-1 and maxShipSizeH >= self.smallestShip-1:
                self.horizontal = True
                self.directionKnown = True

    # If a shot was hit:
    def ShotHit(self, targetPlayer):
        self.hittedMoveCurrent = self.coordinate
        self.currentKilling.append([self.coordinate.x, self.coordinate.y])

        # If the ship is down
        if self.enemyShipsAlive > targetPlayer.checkAlive():

            # Remove empty coords around the killed ship from possibleMoves
            self.ShipKilledUpdateMoves()

        # After hitting 2 times, the Ai knows the ships direction
        if len(self.currentKilling) == 2:
            if self.optimise:
                self.directionKnown = True
                # if self.coordinate x1 == x2 (Vertical)
                if self.currentKilling[0][0] == self.currentKilling[1][0]:
                    self.horizontal = False
                elif self.currentKilling[0][1] == self.currentKilling[1][1]:
                    self.horizontal = True

    # Removes the move from possible moves, if opomisation is True, it removes every useless move from possible moves list
    def UpdateMovesList(self):
        self.movesDone.append([self.coordinate.x, self.coordinate.y])

        # If shoot optimisation is True, remove coordinates from aiMoves that doesn't need to be tried.
        # Because the smallest ship of the opponent doesn't fit there
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
        self.movesTried.clear()
        self.enemyShipsAlive -= 1
        self.lastMove = 0

    #Its the AI's turn to play
    def Turn(self, targetPlayer):
        self.move = False
        self.coordinate = Coordinate([0,0], self.row_size, self.col_size)

        # Ai chose to do a random shot
        if self.lastMove == 0:
            self.RandomMove(targetPlayer)

        # Hitting the rest of the enemy ship
        if self.lastMove == 1:
            if self.MoveXupper(targetPlayer) == 0:
                self.NextMove(False, 0)
                return self.Turn(targetPlayer)

        elif self.lastMove == 2:
            if self.MoveXlower(targetPlayer) == 0:
                self.NextMove(False, 0)
                return self.Turn(targetPlayer)

        elif self.lastMove == 3:
            if self.MoveYupper(targetPlayer) == 0:
                self.NextMove(False, 0)
                return self.Turn(targetPlayer)

        elif self.lastMove == 4:
            if self.MoveYlower(targetPlayer) == 0:
                self.NextMove(False, 0)
                return self.Turn(targetPlayer)

        #Check if a self.coordinate is valid, else retry
        if self.CheckCoord(targetPlayer) == 0:
            return self.Turn(targetPlayer)

        # Take the shot at enemy player
        if self.move:
            result = self.Attack(targetPlayer, self.coordinate)
        else:
            if self.lastMove > 0:
                self.NextMove(False, 0)
            return self.Turn(targetPlayer)

        # Shot was invalid, retry
        if result == -1:
            if self.lastMove == 0:
                print(self)
            else:
                self.NextMove(False, 0)
                print(self)
            return self.Turn(targetPlayer)

        # Shot valid
        else:
            self.UpdateMovesList()

        # Previous shot was random
        if self.lastMove == 0:
            self.hittedMoveStart = self.coordinate
            self.hittedMoveCurrent = self.coordinate

            # Current shot hitted
            if result == 1:
                self.PreviousRandom_CurrentHit()

        # Shot hitted
        if result == 1:
            self.ShotHit(targetPlayer)

        # Missed
        if result == 0 :
            # Previous shot hitted, ship not down, current shot missed, go to next position to take down the rest of the ship.
            if self.lastMove > 0:
                if self.lastMove < 5:
                    self.NextMove(False, 0)
        return



