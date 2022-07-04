from .error import *

class Coordinate():
    # if the given coordinate is a list, it will convert it to a string
    # if the given coordinate is a string, it will convert it to a list
    # it also validates if the given coordinate is allowed
    def __init__(self, coordinate, row_size, col_size):
        self.row_size = row_size
        self.col_size = col_size
        if isinstance(coordinate, list) and self.validateListCoordinate(coordinate):
            self.x = coordinate[0]
            self.y = coordinate[1]
            self.xy = [self.x,self.y]
            self.str = chr(ord('A') + self.x) + str(self.y+1)
        elif self.validateStrCoordinate(coordinate):
            self.x = ord(coordinate[0])-ord('A')
            self.y = int(coordinate[1:])-1
            self.xy = [self.x,self.y]
            self.str = coordinate

    # checks if the given coordinate is a position on the board
    # it does this if the given coordinate is a string type        
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
    
    # checks if the given coordinate is a position on the board
    # it does this if the given coordinate is a list type     
    def validateListCoordinate(self, coordinate):
        if len(coordinate) == 2:
            if isinstance(coordinate[0], int) and isinstance(coordinate[1], int):
                if coordinate[0] >= 0 and coordinate[0] < self.row_size:
                    if coordinate[1] >= 0 and coordinate[1] < self.col_size:
                        return True
                    else:
                        raise CoordinatePlaceError(coordinate[1])
                else:
                    raise CoordinatePlaceError(coordinate[0])
            else:
                raise CoordinateValueError(coordinate)
        else:
            raise CoordinateValueError(coordinate)

    # checks if the other object is an instance of coordinate and has the same xy value as self
    def __eq__(self, other):
        return isinstance(other, Coordinate) and other.xy == self.xy
