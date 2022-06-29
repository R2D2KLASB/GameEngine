from .coordinate import Coordinate
from .error import *
class Board():
    def __init__(self, row_size, col_size):
        self.row_size = row_size
        self.col_size = col_size
        self.board = [['~'] * col_size for x in range(row_size+1)]    

    def updateBoard(self, coordinates, char):
        if isinstance(coordinates, list):
            for coordinate in coordinates:
                self.board[coordinate.x][coordinate.y] = char
        elif isinstance(coordinates, Coordinate):
            self.board[coordinates.x][coordinates.y] = char
       
    def __str__(self):
        string = "\n   " + " ".join(chr(x + ord('A')) for x in range(0, self.col_size )) + "\n"
        for r in range(self.row_size):
            string += str(r + 1) + ("  " if r <= 8 else " ") +  " ".join(str(self.board[c][r]) for c in range(self.col_size)) + "\n"
        return string

    def __repr__(self):
        rows = ["   " + " ".join(chr(x + ord('A')) for x in range(0, self.col_size ))]
        for r in range(self.row_size):
            rows += [str(r + 1) + ("  " if r <= 8 else " ") +  " ".join(str(self.board[c][r]) for c in range(self.col_size))]
        return rows

class shipBoard(Board):
    def __init__(self, row_size, col_size):
        super().__init__(row_size, col_size)
        self.ships = []
        self.targetcoordinates = []

    def validateShipsOrientation(self, coordinates):
        xCoordinates = sorted([coordinate.x for coordinate in coordinates])
        yCoordinates = sorted([coordinate.y for coordinate in coordinates])
        x = all(cordinate == xCoordinates[0] for cordinate in xCoordinates)
        y = all(cordinate == yCoordinates[0] for cordinate in yCoordinates)
        if x != y:
            if x: return all(y-x==1 for x,y in zip(yCoordinates, yCoordinates[1:]))
            if y: return all(y-x==1 for x,y in zip(xCoordinates, xCoordinates[1:]))
        return False

    def createShip(self, coordinates):
        if self.validateShipsOrientation(coordinates):
            newShip = Ship(coordinates)
            if self.validateShipPosition(newShip):
                self.ships += [newShip]
                self.updateBoard(coordinates, '∎')
                return True
            else:
                raise ErrorMessage('Error Ship position')
        raise ErrorMessage('Error ship orientation')

    def validateShipPosition(self, ship):
        for oldShip in self.ships:
            for oldCoordinate in oldShip.coordinates:
                for newCoordinate in ship.coordinates:
                    if newCoordinate.x in range(oldCoordinate.x-1,oldCoordinate.x+2) and newCoordinate.y == oldCoordinate.y or newCoordinate.y in range(oldCoordinate.y-1,oldCoordinate.y+2) and newCoordinate.x == oldCoordinate.x:
                        return False
        return True

    def checkCordinateAnyShip(self, coordinate):
        for ship in self.ships:
            if ship.checkCoordinate(coordinate):
                return ship
        return False


class Ship():
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.size = len(coordinates)
        self.hits = 0
        self.defeated = False
        # False is horizontaal
        # True is verticaal
        self.orientation = self.setOrientation()

    def checkCoordinate(self, coordinate):
        if coordinate in self.coordinates:
            return True
        return False 
    
    def setOrientation(self):
        if self.coordinates[0].x == self.coordinates[1].x:
            self.coordinates = sorted(self.coordinates, key=lambda ship: ship.y)
            return True
        self.coordinates = sorted(self.coordinates, key=lambda ship: ship.x)
        return False

    def hit(self):
        self.hits += 1
        if self.hits == self.size:
            self.defeated = True

    def __repr__(self):
        lst = []
        for coordinate in self.coordinates:
            lst += [coordinate.xy]
        return str(lst)
    
    def __str__(self):
        return self.__repr__()


class targetBoard(Board):
    def __init__(self, row_size, col_size):
        super().__init__(row_size, col_size)
        self.coordinates = []
