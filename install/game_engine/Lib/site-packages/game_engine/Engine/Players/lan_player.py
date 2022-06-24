from .player import *
from ..coordinate import Coordinate

class LANPlayer(Player):
    def __init__(self, row_size, col_size, name, extern_pub, queue):
        super().__init__(row_size, col_size, name)
        self.extern_pub = extern_pub
        self.queue = queue


    def Attack(self, targetPlayer, coordinate):
        if coordinate not in self.targetBoard.coordinates:

            self.extern_pub.send(coordinate.str)
            msg = self.queue.read(wait=True)

            self.targetBoard.coordinates += [coordinate]

            if msg == 'HIT':
                self.targetBoard.updateBoard(coordinate, 'x')
            elif msg == 'SUNK':
                self.targetDefeated += 1
                self.targetBoard.updateBoard(coordinate, 'x')
            elif msg == 'MIS':
                self.targetBoard.updateBoard(coordinate, 'o')
            elif msg == 'LOSE':
                self.targetBoard.updateBoard(coordinate, 'x')
            return True
        raise ErrorMessage('Target Coordinate already used')

    def enemyAttack(self, coordinate):
        result = super().enemyAttack(coordinate)
        self.extern_pub.send(result)