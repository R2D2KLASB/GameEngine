from .error import *

class Coordinate():
    def __init__(self, coordinate, row_size, col_size):
        self.row_size = row_size
        self.col_size = col_size
        if isinstance(coordinate, list) and self.validateDictCoordinate(coordinate):
            self.x = coordinate[0]-1
            self.y = coordinate[1]-1
            self.xy = [self.x,self.y]
            self.str = chr(ord('A') + self.x-1) + str(self.y)
        elif self.validateStrCoordinate(coordinate):
            self.x = ord(coordinate[0])-ord('A')
            self.y = int(coordinate[1:])-1
            self.xy = [self.x,self.y]
            self.str = coordinate
            
    def validateStrCoordinate(self, coordinate):
        if ord(coordinate[0]) >= ord('A') and ord(coordinate[0]) < ord('A') + self.row_size:
            if coordinate[1:].isnumeric():
                if int(coordinate[1:]) > 0 and int(coordinate[1:]) <= self.row_size:
                    return True
                else:
                    raise CoordinatePlaceError(coordinate[1:])
            else:
                raise CoordinateValueError(coordinate)
        else:
            raise CoordinatePlaceError(coordinate[0])
    
    def validateDictCoordinate(self, coordinate):
        if len(coordinate) == 2:
            if isinstance(coordinate[0], int) and isinstance(coordinate[1], int):
                if coordinate[0] > 0 and coordinate[0] <= row_size:
                    if coordinate[1] > 0 and coordinate[1] <= col_size:
                        return True
                    else:
                        raise CoordinatePlaceError(coordinate[1])
                else:
                    raise CoordinatePlaceError(coordinate[0])
            else:
                raise CoordinateValueError(coordinate)
        else:
            raise CoordinateValueError(coordinate)

    def __eq__(self, other):
        return isinstance(other, Coordinate) and other.xy == self.xy
