from .boards import *
from .player import *

import random
class AIPlayer(Player):
    def __init__(self, row_size, col_size, name):
        super().__init__(row_size, col_size, name)
        self.ships = [5, 4, 3, 3, 2]

    def setupBoard(self):
        shipSizes = [5, 4, 3, 3, 2]
        print(self.shipBoard)
        while len(shipSizes) > 0:
            result = False
            while result is False:
                try:
                    print('Available Ships: ' + str(shipSizes))
                    orientation = random.randint(0,1)
                    coordinates = []
                    if orientation == 0:
                        x = random.randint(0,(9-shipSizes[0]))
                        y = random.randint(0,9)
                        for i in range(shipSizes[0]):
                            cor = [x,y+i]
                            coordinates+=[Coordinate(cor, self.row_size, self.col_size)]
                    else:
                        x = random.randint(0,9)
                        y = random.randint(0,(9-shipSizes[0]))
                        for i in range(shipSizes[0]):
                            cor = [x+i,y]
                            coordinates+=[Coordinate(cor, self.row_size, self.col_size)]
                    if len(coordinates) in shipSizes:
                        print(coordinates)
                        result = self.shipBoard.createShip(coordinates)
                        if result:
                            shipSizes.remove(len(coordinates))
                        clear()
                    
                except Exception as e:
                    clear()
                    print(e)
                    pass
        print(self)
            

    
    def Turn(self, targetPlayer):
        x = random.randint(0,10)
        y = random.randint(0,10)
        cor = [x,y]
        coordinate = Coordinate(cor, self.row_size, self.col_size)
        self.Attack(targetPlayer, coordinate)
            
            



