from ..boards import *
from .player import Player
import time

import random
class AIPlayer(Player):
    def __init__(self, row_size, col_size, name):
        super().__init__(row_size, col_size, name)


    def Attack(self, targetPlayer, coordinate):
        if coordinate not in self.targetBoard.coordinates:
            self.targetBoard.coordinates += [coordinate]
            if targetPlayer.enemyAttack(coordinate):
                self.targetBoard.updateBoard(coordinate, 'x')
            else:
                self.targetBoard.updateBoard(coordinate, 'o')
            return True
        raise ErrorMessage('Target Coordinate already used')

    def setupBoard(self):
        shipSizes = [2]
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
                    print(e)
                    pass
            

    
    def Turn(self, targetPlayer):
        result = False
        while result is False:
            try:
                x = random.randint(0,self.row_size-1)
                y = random.randint(0,self.col_size-1)
                cor = [x,y]
                coordinate = Coordinate(cor, self.row_size, self.col_size)
                while coordinate in self.targetBoard.coordinates:
                    x = random.randint(0,self.row_size-1)
                    y = random.randint(0,self.col_size-1)
                    cor = [x,y]
                    coordinate = Coordinate(cor, self.row_size, self.col_size)
                result = self.Attack(targetPlayer, coordinate)
            except Exception as e:
                    print(e)
                    time.sleep(5)
                    pass
                    clear()
        clear()
            
            



