from .ai import AIPlayer
from ..error import *

class LANAI(AIPlayer):
    def __init__(self, row_size, col_size, name, connect, optimalisation=True):
        super().__init__(row_size, col_size, name, optimalisation)
        self.connect = connect
        self.connect.PublishSetup(self.shipBoard.ships)
        

    def setupBoard(self):
        super().setupBoard()
        print(self)

    def Attack(self, targetPlayer, coordinate):
        if coordinate not in self.targetBoard.coordinates:
            self.targetBoard.coordinates += [coordinate]
            msg = self.connect.sendFire(coordinate)
            # clear()
            print(self)
            if msg == 'HIT':
                self.connect.getHit(coordinate)
                self.targetBoard.updateBoard(coordinate, 'x')
                return 1
            elif msg == 'MISS':
                self.connect.getSunk(coordinate)
                self.targetBoard.updateBoard(coordinate, 'o')
                return 0
            elif msg == 'SUNK':
                self.connect.getMiss(coordinate)
                self.targetBoard.updateBoard(coordinate, 'x')
                self.targetDefeated += 1
                targetPlayer.shipSizes.remove(targetPlayer.shipSizes[0])
                coords = []
                for i in range(self.row_size):
                    if coordinate.y + i < 10:
                        if self.targetBoard.board[coordinate.x][coordinate.y + i] == 'x':
                            if not [coordinate.x,coordinate.y + i] in coords:
                                coords.append([coordinate.x + i,coordinate.y])
                        else:
                            break;
                for i in range(self.row_size):
                    if coordinate.y - i >= 0:
                        if self.targetBoard.board[coordinate.x][coordinate.y - i] == 'x':
                            if not [coordinate.x, coordinate.y - i] in coords:
                                coords.append([coordinate.x - i,coordinate.y])
                        else:
                            break;
                for i in range(self.row_size):
                    if coordinate.x + i < 10:
                        if self.targetBoard.board[coordinate.x + i][coordinate.y] == 'x':
                            if not [coordinate.x + i, coordinate.y] in coords:
                                coords.append([coordinate.x,coordinate.y + i])
                        else:
                            break;
                for i in range(self.row_size):
                    if coordinate.x - i >= 0:
                        if self.targetBoard.board[coordinate.x - i][coordinate.y] == 'x':
                            if not [coordinate.x - 1, coordinate.y] in coords:
                                coords.append([coordinate.x - i, coordinate.y])
                        else:
                            break;
                print("Ship sunk: " + str(coords))
                if len(coords) in self.enemyShips:
                    print(len(coords)-1)
                    self.enemyShips.remove(len(coords)-1)

                return 1
            elif msg == 'LOSE':
                self.connect.getLose(coordinate)
                self.targetBoard.updateBoard(coordinate, 'x')
                self.targetDefeated += 1
                return 1
        return -1
        raise ErrorMessage('Target Coordinate already used')

    def enemyAttack(self, coordinate):
        result = super().enemyAttack(coordinate)
        self.connect.sendExtern(result)
        if result == 'HIT':
            self.connect.sendHit(coordinate)
        elif result == 'SUNK':
            self.connect.sendSunk(coordinate)
        elif result == 'MISS':
            self.connect.sendMiss(coordinate)
        # clear()
        print(self)