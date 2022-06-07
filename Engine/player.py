from .coordinate import *
from .boards import *

class Player():
    def __init__(self, row_size, col_size, name):
        self.shipBoard = shipBoard(row_size,col_size)
        self.targetBoard = targetBoard(row_size,col_size)
        self.row_size = row_size
        self.col_size = col_size
        self.name = name
        self.setupBoard()

    def setupBoard(self):
        shipSizes = [2, 3]
        print(self.shipBoard)
        while len(shipSizes) > 0:
            print('Available Ships: ' + str(shipSizes))
            coordinates = [Coordinate(cor, self.row_size, self.col_size) for cor in input("Ship Coordinates:").upper().split(',')]
            if len(coordinates) in shipSizes:
                if self.shipBoard.createShip(coordinates):
                    shipSizes.remove(len(coordinates))
                else:
                    print('Try again')
            else:
                print("Error ship size")
        print(self)

    def Turn(self, targetPlayer):
        coordinate = Coordinate(input("Ship Coordinates:", self.row_size, self.col_size).upper())
        self.Attack(targetPlayer, coordinate)
    
    def Attack(self, targetPlayer, coordinate):
        if coordinate not in self.targetBoard.coordinates:
            self.targetBoard.coordinates += [coordinate]
            if targetPlayer.enemyAttack(coordinate):
                self.targetBoard.updateBoard(coordinate, 'x')
            else:
                self.targetBoard.updateBoard(coordinate, 'o')
            return True
        raise CoordinatePlaceError(coordinate)
    
    def enemyAttack(self, coordinate):
        if coordinate not in self.shipBoard.targetcoordinates:
            self.shipBoard.targetcoordinates += [coordinate]
            hittedShip = self.shipBoard.checkCordinateAnyShip(coordinate)
            if hittedShip:
                hittedShip.hit()
                self.shipBoard.updateBoard(coordinate, 'x')
                return True
            else:
                self.shipBoard.updateBoard(coordinate, 'o')
                return False
        raise CoordinatePlaceError(coordinate)

    def checkDefeated(self):
        return all(ship.defeated for ship in self.shipBoard.ships)

    def checkAlive(self):
        return sum([not ship.defeated for ship in self.shipBoard.ships])
        

    def __str__(self):
        string = 'Shipboard:                      Targetboard:\n'
        for row in range(self.row_size):
            string += self.shipBoard.__repr__()[row] + "\t\t" + self.targetBoard.__repr__()[row] + "\n"
        string += 'Ships alive: ' + str(self.checkAlive())
        return string


    def __repr__(self):
        return self.__str__()


