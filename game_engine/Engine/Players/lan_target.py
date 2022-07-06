from .player import *

# copy of the player class with a few tweaks in some functions to be able to play over lan
class LANTarget(Player):
    def __init__(self, row_size, col_size, name, publisher, queue):
        super().__init__(row_size, col_size, name)
        self.publisher = publisher
        self.queue = queue

    def Turn(self, targetPlayer):
        print('\nWaiting on next move from the other player...')
        self.publisher['intern'].send('TEXT Waiting on enemy move..')
        msg = self.queue.read(wait=True)
        print(msg)
        # clear()
        self.Attack(targetPlayer, Coordinate(msg, self.row_size, self.col_size))

    def Attack(self, targetPlayer, coordinate):
        
        self.targetBoard.coordinates += [coordinate]
        if targetPlayer.enemyAttack(coordinate):
            self.targetBoard.updateBoard(coordinate, 'x')
        else:
            self.targetBoard.updateBoard(coordinate, 'o')
        return True

    def checkDefeated(self):
        if self.checkAlive == 0:
            return True
        return False
    

    def checkAlive(self):
        return len(self.shipSizes)

    def setupBoard(self):
        return