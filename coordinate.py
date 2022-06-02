
class CoordinateValueError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '{} is invalid input, CoordinateValue can only accept ' \
               'A string with first index an char followed by an integer or a dict with two integers'.format(self.value)

class CoordinatePlaceError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '{} is invalid input, The Coordinate Place is not allowed '.format(self.value)

class Coordinate():
    def __init__(self, coordinate):
        if isinstance(coordinate, list) and self.validateDictCoordinate(coordinate):
            self.x = coordinate[0]
            self.y = coordinate[1]
            self.xy = [self.x,self.y]
            self.str = chr(ord('A') + self.x-1) + str(self.y)
        elif self.validateStrCoordinate(coordinate):
            self.x = ord(coordinate[0])-ord('A')+1
            self.y = int(coordinate[1:])
            self.xy = [self.x,self.y]
            self.str = coordinate
            
    def validateStrCoordinate(self, coordinate):
        if ord(coordinate[0]) >= ord('A') and ord(coordinate[0]) < ord('A') + 10:
            if coordinate[1:].isnumeric():
                if int(coordinate[1:]) > 0 and int(coordinate[1:]) <= 10:
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
                if coordinate[0] > 0 and coordinate[0] <= 10:
                    if coordinate[1] > 0 and coordinate[1] <= 10:
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
