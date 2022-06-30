from .ai import AIPlayer

class LANAI(AIPlayer):
    def __init__(self, row_size, col_size, name, publisher, queue, camera=False):
        super().__init__(row_size, col_size, name, camera)

        self.publisher = publisher
        self.queue = queue
        self.PublishSetup()
        

    def PublishSetup(self):
        shipgcode = [('G6 R%s C%s W%s L%s' % ((ship.coordinates[0].y+1), (ship.coordinates[0].x+1),(1 if ship.orientation else ship.size),(ship.size if ship.orientation else 1))) for ship in self.shipBoard.ships]
        shipCoordinates = []
        for ship in self.shipBoard.ships:
            for coordinate in ship.coordinates:
                shipCoordinates += [coordinate.xy]
        self.publisher['intern'].send('boats')
        self.publisher['intern'].send(str(shipCoordinates).replace(' ', ''))
        self.publisher['gcode'].send(('\n'.join(shipgcode))+'\nG28\n')

        