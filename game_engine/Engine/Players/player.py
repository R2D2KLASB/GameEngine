from ..coordinate import *
from ..boards import *
from ..error import *

class Player():
    def __init__(self, row_size, col_size, name, shiplist=False):
        self.shipBoard = shipBoard(row_size,col_size)
        self.targetBoard = targetBoard(row_size,col_size)
        self.row_size = row_size
        self.col_size = col_size
        self.name = name
        self.shiplist = shiplist
        self.shipSizes = [2,3]
        self.countShips = len(self.shipSizes)
        self.targetDefeated = 0
        self.setupBoard()

    def setupBoard(self):
        while len(self.shipSizes) > 0:
            result = False
            while result is False:
                try:
                    if self.shiplist:
                        for ship in self.shiplist:
                            coordinates = [Coordinate(coordinate, self.row_size, self.col_size) for cordinate in ship]
                            if len(coordinates) in self.shipSizes:
                                result = self.shipBoard.createShip(coordinates)
                                self.shipSizes.remove(len(coordinates))
                        else:
                            raise ErrorMessage("Error ship size")
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

    def Turn(self, targetPlayer):
        # clear()
        print('It\'s your turn!')
        result = False
        while result is False:
            try:
                print(self)
                coordinate = Coordinate(input("Attack Coordinate:").upper(), self.row_size, self.col_size)
                result = self.Attack(targetPlayer, coordinate)
                clear()
                print(self)
            except Exception as e:
                clear()
                print(e)
                pass
                
    
    def Attack(self, targetPlayer, coordinate):
        if coordinate not in self.targetBoard.coordinates:
            self.targetBoard.coordinates += [coordinate]
            result = targetPlayer.enemyAttack(coordinate)
            if result == 'HIT':
                self.targetBoard.updateBoard(coordinate, 'x')
            elif result == 'MIS':
                self.targetBoard.updateBoard(coordinate, 'o')
            elif result == 'SUNK':
                self.targetBoard.updateBoard(coordinate, 'x')
                self.targetDefeated += 1
            return True
        raise ErrorMessage('Target Coordinate already used')
    
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

    def checkDefeated(self):
        return all(ship.defeated for ship in self.shipBoard.ships)

    def checkAlive(self):
        return sum([not ship.defeated for ship in self.shipBoard.ships])
        

    def __str__(self):
        string = '\n' + self.name + ':\n\nShipboard:                      Targetboard:\n'
        for row in range(self.row_size+1):
            string += self.shipBoard.__repr__()[row] + "\t\t" + self.targetBoard.__repr__()[row] + "\n"
        string += 'Ships alive: ' + str(self.checkAlive()) + "                  Defeated:" + str(self.targetDefeated)
        return string


    def __repr__(self):
        return self.__str__()



