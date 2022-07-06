from .player import *
from ..coordinate import Coordinate
import time

# copy of the player class with a few tweaks in some functions to be able to play over lan
class LANPlayer(Player):
    def __init__(self, row_size, col_size, name, connect, camera):
        super().__init__(row_size, col_size, name, camera)
        self.connect = connect
        self.connect.PublishSetup(self.shipBoard.ships)

    def Turn(self, targetPlayer):
        # clear()
        # print('It\'s your turn!!')
        # print(self)
        # coordinate = self.connect.getPos(self.row_size, self.col_size)
        # if coordinate:
        #     result = self.Attack(targetPlayer, coordinate)
        #     clear()
        #     print(self)
        # else:
            super().Turn(targetPlayer)

    def Attack(self, targetPlayer, coordinate):
        if coordinate not in self.targetBoard.coordinates:
            msg = self.connect.sendFire(coordinate)
            time.sleep(3.5)
            self.targetBoard.coordinates += [coordinate]
            if msg == 'HIT':
                self.connect.getHit(coordinate)
                self.targetBoard.updateBoard(coordinate, 'x')
            elif msg == 'SUNK':
                self.connect.getSunk(coordinate)
                self.targetDefeated += 1
                self.targetBoard.updateBoard(coordinate, 'x')
            elif msg == 'MISS':
                self.connect.getMiss(coordinate)
                self.targetBoard.updateBoard(coordinate, 'o')
            elif msg == 'LOSE':
                self.connect.getLose(coordinate)
                self.targetBoard.updateBoard(coordinate, 'x')
            return True
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

    def checkDefeated(self):
        result = all(ship.defeated for ship in self.shipBoard.ships)
        if result:
            self.connect.sendLose()
        return result