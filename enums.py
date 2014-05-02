from enum import Enum

#color enum represents color of each game piece
class Color(Enum):
    blank = 0
    white = 1
    black = 2

    @staticmethod
    def from_int(num):
        colors = list(Color)
        filtered = [x for x in colors if x.value==num]
        if len(filtered) == 1:
            return filtered[0]
        else:
            raise Exception('Enumeration does not contain that value.')

    #method on enum allows getting the opposite color (could have used booleans)
    @staticmethod
    def opposite(color):
        if color is Color.black:
            return Color.white
        elif color is Color.white:
            return Color.black
        else:
            return color
