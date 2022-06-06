from coordinate import *
import boards

class Player():
    def __init__(self, row_size, col_size, name):
        self.shipBoard = boards.shipBoard(row_size,col_size)
        self.targetBoard = boards.targetBoard(row_size,col_size)
        self.row_size = row_size
        self.col_size = col_size
        self.name = name
        self.setupBoard()

    def setupBoard(self):
        shipSizes = [2]
        print(self.shipBoard)
        while len(shipSizes) > 0:
            print('Available Ships: ' + str(shipSizes))
            coordinates = [Coordinate(cor) for cor in input("Ship Coordinates:").upper().split(',')]
            if len(coordinates) in shipSizes:
                self.shipBoard.createShip(coordinates)
                shipSizes.remove(len(coordinates))
            else:
                print("Error ship size")
        print(self)

    def Turn(self, targetPlayer):
        coordinate = Coordinate(input("Ship Coordinates:").upper())
        self.Attack(targetPlayer, coordinate)
    
    def Attack(self, targetPlayer, coordinate):
        if coordinate not in self.targetBoard.coordinates:
            self.targetBoard.coordinates += [coordinate]
            if targetPlayer.enemyAttack(coordinate):
                self.targetBoard.updateBoard(coordinate, 'x')
            else:
                self.targetBoard.updateBoard(coordinate, 'o')
            return True
        else:
            raise CoordinatePlaceError(coordinate)
    
    def enemyAttack(self, coordinate):
        if coordinate not in self.shipBoard.targetcoordinates:
            self.shipBoard.targetcoordinates += [coordinate]
            if self.shipBoard.checkCordinateAnyShip(coordinate):
                self.shipBoard.updateBoard(coordinate, 'x')
                return True
            else:
                self.shipBoard.updateBoard(coordinate, 'o')
                return False
        else:
            raise CoordinatePlaceError(coordinate[0])
        

    def __str__(self):
        string = 'Shipboard:                      Targetboard:\n'
        for row in range(self.row_size):
            string += self.shipBoard.__repr__()[row] + "\t\t" + self.targetBoard.__repr__()[row] + "\n"
        return string


    def __repr__(self):
        return self.__str__()


