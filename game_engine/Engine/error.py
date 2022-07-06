import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# class to give feedback about a coordinate value error
class CoordinateValueError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return '\n{} is invalid input, CoordinateValue can only accept ' \
               'A string with first index an char followed by an integer or a dict with two integers'.format(self.value)

# class to give feedback about a coordinate place error
class CoordinatePlaceError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return '\n{} is invalid input, The Coordinate Place is not allowed '.format(self.value)

# general class to give feedback about an error
class ErrorMessage(Exception):
    def __init__(self, value, publisher=False):
        self.value = value
        if publisher:
            publisher.send('TEXT ' + value)

    def __str__(self):
        return '\n' + str(self.value)