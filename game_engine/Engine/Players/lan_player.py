from .player import Player
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
            elif msg == 'MIS':
                self.targetBoard.updateBoard(coordinate, 'o')
            return True
        raise ErrorMessage('Target Coordinate already used')

    def enemyAttack(self, coordinate):
        if super().enemyAttack(coordinate):
            self.extern_pub.send('HIT')
        else:
            self.extern_pub.send('MIS')