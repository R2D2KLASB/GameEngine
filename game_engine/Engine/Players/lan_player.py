from .player import *
from ..coordinate import Coordinate
import time

class LANPlayer(Player):
    def __init__(self, row_size, col_size, name, publisher, queue):
        super().__init__(row_size, col_size, name)
        self.publisher = publisher
        self.queue = queue
        # self.intern_pub.send(str([ship for ship in self.shipBoard.ships]))
        self.shipgcode = [('G6 R%s C%s W%s L%s' % ((ship.coordinates[0].y+1), (ship.coordinates[0].x+1),(1 if ship.orientation else ship.size),(ship.size if ship.orientation else 1))) for ship in self.shipBoard.ships]
        self.publisher['gcode'].send(('\n'.join(self.shipgcode))+'\nG28\n')


    def Attack(self, targetPlayer, coordinate):
        if coordinate not in self.targetBoard.coordinates:
            self.publisher['intern'].send('FIRE')
            self.publisher['extern'].send(coordinate.str)
            msg = self.queue.read(wait=True)
            # time.sleep(3.5)
            self.targetBoard.coordinates += [coordinate]
            if msg == 'HIT':
                self.publisher['intern'].send('HIT 0')
                self.publish['gcode'].send('G4 R%s C%s P0' % (coordinate.y+1, coordinate.x+1))
                self.targetBoard.updateBoard(coordinate, 'x')
            elif msg == 'SUNK':
                self.publisher['intern'].send('HIT 0')
                self.publish['gcode'].send('G4 R%s C%s P0' % (coordinate.y+1, coordinate.x+1))
                # time.sleep(4.5)
                self.publisher['intern'].send('SUNK 0')
                self.targetDefeated += 1
                self.targetBoard.updateBoard(coordinate, 'x')
            elif msg == 'MISS':
                self.publisher['intern'].send('MISS 0')
                self.publish['gcode'].send('G5 R%s C%s P0' % (coordinate.y+1, coordinate.x+1))
                self.targetBoard.updateBoard(coordinate, 'o')
            elif msg == 'LOSE':
                # self.publisher['extern'].send('WON')
                self.publisher['intern'].send('WIN')
                self.publish['gcode'].send('G8 P1')
                self.targetBoard.updateBoard(coordinate, 'x')
            return True
        raise ErrorMessage('Target Coordinate already used')

    def enemyAttack(self, coordinate):
        result = super().enemyAttack(coordinate)
        self.publisher['extern'].send(result)
        if result == 'HIT':
            self.publisher['intern'].send('HIT 1')
            self.publish['gcode'].send('G4 R%s C%s P1' % (coordinate.y+1, coordinate.x+1))
        elif result == 'SUNK':
            self.publish['gcode'].send('G4 R%s C%s P1' % (coordinate.y+1, coordinate.x+1))
            for ship in self.shipBoard.ships:
                if ship.checkCoordinate(coordinate):
                    sunkedShip = ship
                    break
            self.publish['gcode']('G7 R%s C%s W%s L%s P1' % ((sunkedShip.coordinates[0].y+1), (sunkedShip.coordinates[0].x+1),(1 if sunkedShip.orientation else sunkedShip.size),(sunkedShip.size if sunkedShip.orientation else 1)))
        elif result == 'MISS':
            self.publish['gcode'].send('G5 R%s C%s P1' % (coordinate.y+1, coordinate.x+1))

    def checkDefeated(self):
        result = all(ship.defeated for ship in self.shipBoard.ships)
        if result:
            self.publisher['intern'].send('LOSE')
            self.publisher['gcode'].send('G8 P0')
        return result