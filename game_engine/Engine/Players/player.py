from ..coordinate import *
from ..boards import *
from ..error import *
from ...Camera import *
import time

class Player():
    # initializes the player, board size specified, player name and the use of camera as bool
    def __init__(self, row_size, col_size, name, camera=False):
        self.shipBoard = shipBoard(row_size,col_size)
        self.targetBoard = targetBoard(row_size,col_size)
        self.row_size = row_size
        self.col_size = col_size
        self.name = name
        self.camera = camera
        self.shipSizes = [2, 3, 3, 4, 5]
        self.countShips = len(self.shipSizes)
        self.targetDefeated = 0
        self.setupBoard()

    # the setup of the board. It will use the camera if specified, else it will use given coordinates by typing in console
    # there are checks if all boats specified are setup
    def setupBoard(self):
        while len(self.shipSizes) > 0:
            result = False
            while result is False:
                try:
                    if self.camera:
                        shiplist = self.camera.webcam_detection()
                        for ship in shiplist:
                            coordinates = [Coordinate([coordinate[1], coordinate[0]], self.row_size, self.col_size) for coordinate in ship]
                            if len(coordinates) in self.shipSizes:
                                result = self.shipBoard.createShip(coordinates)
                                self.shipSizes.remove(len(coordinates))
                            else:
                                self.shipSizes = [2, 3, 3, 4, 5]
                                self.shipBoard.ships = []
                                raise ErrorMessage("Error image detection.. Try again")
                    else:
                        print('\n' + self.name + ' Setup Ships')
                        print(self.shipBoard)
                        print('Available Ships: ' + str(self.shipSizes))
                        coordinates = [Coordinate(cor, self.row_size, self.col_size) for cor in input("Ship Coordinates:").upper().split(',')]
                        if len(coordinates) in self.shipSizes:
                            result = self.shipBoard.createShip(coordinates)
                            self.shipSizes.remove(len(coordinates))
                            clear()
                        else:
                            raise ErrorMessage("Error ship size")
                except Exception as e:
                    clear()
                    print(e)
                    pass
        print(self)

    # turn function to give where you want to place your missile
    def Turn(self, targetPlayer):
        # clear()
        print('It\'s your turn!')
        result = False
        while result is False:
            try:
                print(self)
                coordinate = Coordinate(input("Attack Coordinate:").upper(), self.row_size, self.col_size)
                result = self.Attack(targetPlayer, coordinate)
                # clear()
                print(self)
            except Exception as e:
                clear()
                print(e)
                pass
                
    # attack function to check if given coordinate is a hit or miss and if the boat has sunk
    # given target player is the opponent
    def Attack(self, targetPlayer, coordinate):
        if coordinate not in self.targetBoard.coordinates:
            self.targetBoard.coordinates += [coordinate]
            result = targetPlayer.enemyAttack(coordinate)
            if result == 'HIT':
                self.targetBoard.updateBoard(coordinate, 'x')
            elif result == 'MISS':
                self.targetBoard.updateBoard(coordinate, 'o')
            elif result == 'SUNK':
                self.targetBoard.updateBoard(coordinate, 'x')
                self.targetDefeated += 1
            return True
        raise ErrorMessage('Target Coordinate already used')
    
    # enemy attack to return to opponent if he/she hitted or missed
    def enemyAttack(self, coordinate):
        tmpAlive = self.checkAlive()
        self.shipBoard.targetcoordinates += [coordinate]
        hittedShip = self.shipBoard.checkCordinateAnyShip(coordinate)
        if hittedShip:
            hittedShip.hit()
            self.shipBoard.updateBoard(coordinate, 'x')
            if self.checkDefeated():
                return 'LOSE'
            elif tmpAlive != self.checkAlive():
                return 'SUNK'
            else:
                return 'HIT'
        else:
            self.shipBoard.updateBoard(coordinate, 'o')
            return 'MISS'

    # check if all ships are defeated
    def checkDefeated(self):
        return all(ship.defeated for ship in self.shipBoard.ships)

    # give the numbers of boats still alive
    def checkAlive(self):
        return sum([not ship.defeated for ship in self.shipBoard.ships])
        
    # general print for printing the boards with ships alive or defeated
    def __str__(self):
        string = '\n' + self.name + ':\n\nShipboard:                      Targetboard:\n'
        for row in range(self.row_size+1):
            string += self.shipBoard.__repr__()[row] + "\t\t" + self.targetBoard.__repr__()[row] + "\n"
        string += 'Ships alive: ' + str(self.checkAlive()) + "                  Defeated:" + str(self.targetDefeated)
        return string


    def __repr__(self):
        return self.__str__()



