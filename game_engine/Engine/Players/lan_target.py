from .player import *

class LANTarget(Player):
    def __init__(self, row_size, col_size, name, extern_pub, queue):
        super().__init__(row_size, col_size, name)
        self.extern_pub = extern_pub
        self.queue = queue

    def Turn(self, targetPlayer):
        msg = self.queue.read(wait=True)
        result = self.Attack(targetPlayer, Coordinate(msg, self.row_size, self.col_size))

    def Attack(self, targetPlayer, coordinate):
        
        self.targetBoard.coordinates += [coordinate]
        if targetPlayer.enemyAttack(coordinate):
            self.targetBoard.updateBoard(coordinate, 'x')
        else:
            self.targetBoard.updateBoard(coordinate, 'o')
        return True
    

    def checkDefeated(self):
        return False

    def checkAlive(self):
        return 4

    def setupBoard(self):
        return