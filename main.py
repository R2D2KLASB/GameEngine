import re
from coordinate import Coordinate
import boards

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
        self.shipBoard = boards.shipBoard(row_size,col_size)
        self.targetBoard = boards.targetBoard(row_size,col_size)
        self.row_size = row_size
        self.col_size = col_size
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
    
    def Attack(self, player, targetplayer, coordinate):
        if coordinate in targetplayer.shipBoard.ships:
            self.targetBoard.hitcoordinates += coordinate
        else:
            self.targetBoard.misscoordinates += coordinate
    
    def enemyAttack(self, coordinate):
        targetship = self.shipBoard.checkCordinateAnyShip(coordinate)
        if targetship:
            targetship.hitcoordinates += coordinate
            return True
        else:
            self.shipBoard.misscoordinates += coordinate
            return False



    def __str__(self):
        string = 'Shipboard:                      Targetboard:\n'
        for row in range(self.row_size):
            string += self.shipBoard.__repr__()[row] + "\t\t" + self.targetBoard.__repr__()[row] + "\n"
        return string


    def __repr__(self):
        return self.__str__()


   

gameEngine = GameEngine()
