from .coordinate import *
from .boards import *
from .error import *

class Player():
    def __init__(self, row_size, col_size, name):
        self.shipBoard = shipBoard(row_size,col_size)
        self.targetBoard = targetBoard(row_size,col_size)
        self.row_size = row_size
        self.col_size = col_size
        self.name = name
        self.setupBoard()

    def setupBoard(self):
        shipSizes = [5,4,3,2]
        while len(shipSizes) > 0:
            result = False
            while result is False:
                try:
                    print('\n' + self.name + ' Setup Ships')
                    print(self.shipBoard)
                    print('Available Ships: ' + str(shipSizes))
                    coordinates = [Coordinate(cor, self.row_size, self.col_size) for cor in input("Ship Coordinates:").upper().split(',')]
                    if len(coordinates) in shipSizes:
                        result = self.shipBoard.createShip(coordinates)
                        shipSizes.remove(len(coordinates))
                        clear()
                    else:
                        raise ErrorMessage("Error ship size")
                except Exception as e:
                    clear()
                    print(e)
                    pass
        print(self)

    def Turn(self, targetPlayer):
        result = False
        while result is False:
            try:
                # print(self)
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
            if targetPlayer.enemyAttack(coordinate):
                self.targetBoard.updateBoard(coordinate, 'x')
            else:
                self.targetBoard.updateBoard(coordinate, 'o')
            return True
        else:
            return False
        raise ErrorMessage('Target Coordinate already used')
    
    def enemyAttack(self, coordinate):
        self.shipBoard.targetcoordinates += [coordinate]
        hittedShip = self.shipBoard.checkCordinateAnyShip(coordinate)
        if hittedShip:
            hittedShip.hit()
            self.shipBoard.updateBoard(coordinate, 'x')
            if "ai" not in self.name:
                print(self)
            return True
        else:
            self.shipBoard.updateBoard(coordinate, 'o')
            if "ai" not in self.name:
                print(self)
            return False

    def checkDefeated(self):
        return all(ship.defeated for ship in self.shipBoard.ships)

    def checkAlive(self):
        return sum([not ship.defeated for ship in self.shipBoard.ships])
        

    def __str__(self):
        string = '\n' + self.name + ':\n\nShipboard:              Targetboard:\n'
        for row in range(self.row_size+1):
            string += self.shipBoard.__repr__()[row] + "\t\t" + self.targetBoard.__repr__()[row] + "\n"
        string += 'Ships alive: ' + str(self.checkAlive())
        return string


    def __repr__(self):
        return self.__str__()



