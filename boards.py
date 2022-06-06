from coordinate import Coordinate

class Board():
    def __init__(self, row_size, col_size):
        self.row_size = row_size
        self.col_size = col_size
        self.board = [[0] * col_size for x in range(row_size)]    
       
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
        self.misscoordinates = []
        self.hitcoordinates = []

    def validateShipsOrientation(self, coordinates):
        xCoordinates = sorted([coordinate.x for coordinate in coordinates])
        yCoordinates = sorted([coordinate.y for coordinate in coordinates])
        x = all(cordinate == xCoordinates[0] for cordinate in xCoordinates)
        y = all(cordinate == yCoordinates[0] for cordinate in yCoordinates)
        if x != y:
            if x: return all(y-x==1 for x,y in zip(yCoordinates, yCoordinates[1:]))
            if y: return all(y-x==1 for x,y in zip(xCoordinates, xCoordinates[1:]))
        return False

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

    def __str__(self):
        string = "\n   " + " ".join(chr(x + ord('A')) for x in range(0, self.col_size )) + "\n"
        for r in range(self.row_size):
            string += str(r + 1) + ("  " if r <= 8 else " ") +  " ".join(str('-' if self.checkCordinateAnyShip(Coordinate([c+1,r+1])) else self.board[c][r]) for c in range(self.col_size)) + "\n"
        return string

    def __repr__(self):
        rows = ["   " + " ".join(chr(x + ord('A')) for x in range(0, self.col_size ))]
        for r in range(self.row_size):
            rows += [str(r + 1) + ("  " if r <= 8 else " ") +  " ".join(str('-' if self.checkCordinateAnyShip(Coordinate([c+1,r+1])) else self.board[c][r]) for c in range(self.col_size))]
        return rows


class Ship():
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.size = len(coordinates)

    def checkCoordinate(self, coordinate):
        if coordinate in self.coordinates:
            return True
        return False 

class targetBoard(Board):
    def __init__(self, row_size, col_size):
        super().__init__(row_size, col_size)
        self.hitcoordinates = []
        self.misscoordinates = []
