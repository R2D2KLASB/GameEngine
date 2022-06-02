import re
from coordinate import Coordinate

class GameEngine():
    def __init__(self):
        self.row_size = 10
        self.col_size = 10
        print('Player 1 Setup Ships')
        self.player1 = Player(self.row_size, self.col_size)
        print('Player 2 Setup Ships')
        self.player2 = Player(self.row_size, self.col_size)



class Player():
    def __init__(self, row_size, col_size):
        self.shipBoard = shipBoard(row_size,col_size)
        self.targetBoard = targetBoard(row_size,col_size)
        self.row_size = row_size
        self.col_size = col_size
        self.setupBoard()

    def setupBoard(self):
        shipSizes = [2]
        print(self.shipBoard)
        while len(shipSizes) > 0:
            print('Available Ships: ' + str(shipSizes))
            coordinates = [Coordinate(cor) for cor in input("Ship Coordinates:").upper().split(',')]
            if self.shipBoard.validateShipsOrientation(coordinates):
                if len(coordinates) in shipSizes:
                    newShip = Ship(coordinates)
                    if self.shipBoard.validateShipPosition(newShip):
                        self.shipBoard.ships += [newShip]
                        shipSizes.remove(len(coordinates))
                        if len(shipSizes) >= 1:
                            print(self.shipBoard)
                    else:
                        print('Error Ship position')
                else:
                    print("Error ship size")
            else:
                print('Error ship orientation')
        print(self)
    
    def Attack(self, player, targetplayer, coordinate):
        if coordinate in player.targetBoard.coordinates:
            return False
        else:
            player.targetBoard.coordinates += coordinate



    def __str__(self):
        string = 'Shipboard:                      Targetboard:\n'
        for row in range(self.row_size):
            string += self.shipBoard.__repr__()[row] + "\t\t" + self.targetBoard.__repr__()[row] + "\n"
        return string


    def __repr__(self):
        return self.__str__()


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

    def validateShipsOrientation(self, coordinates):
        xCoordinates = sorted([coordinate.x for coordinate in coordinates])
        yCoordinates = sorted([coordinate.y for coordinate in coordinates])
        x = all(cordinaat == xCoordinates[0] for cordinaat in xCoordinates)
        y = all(cordinaat == yCoordinates[0] for cordinaat in yCoordinates)
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

    def checkCordinaatAnyShip(self, coordinate):
        return any(ship.checkCoordinate(coordinate) for ship in self.ships)

    def __str__(self):
        string = "\n   " + " ".join(chr(x + ord('A')) for x in range(0, self.col_size )) + "\n"
        for r in range(self.row_size):
            string += str(r + 1) + ("  " if r <= 8 else " ") +  " ".join(str('-' if self.checkCordinaatAnyShip(Coordinate([c+1,r+1])) else self.board[c][r]) for c in range(self.col_size)) + "\n"
        return string

    def __repr__(self):
        rows = ["   " + " ".join(chr(x + ord('A')) for x in range(0, self.col_size ))]
        for r in range(self.row_size):
            rows += [str(r + 1) + ("  " if r <= 8 else " ") +  " ".join(str('-' if self.checkCordinaatAnyShip(Coordinate([c+1,r+1])) else self.board[c][r]) for c in range(self.col_size))]
        return rows

class Ship():
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.hitcoordinates = []
        self.size = len(coordinates)

    def checkCoordinate(self, coordinate):
        if coordinate in self.coordinates:
            return True
        return False    

class targetBoard(Board):
    def __init__(self, row_size, col_size):
        super().__init__(row_size, col_size)
        self.coordinates = []




gameEngine = GameEngine()
