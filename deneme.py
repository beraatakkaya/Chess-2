from enum import Enum
from pprint import pprint
from copy import deepcopy

print = pprint


class PieceType(Enum):
    KNIGHT = "knight.png"
    ROOK = "rook.png"

class PieceColor(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0 , 0)

class Piece:
    def __init__(self, location, type, color):
        self.location = location
        self.type = type
        self.color = color

    def set_location(self, new_location):
        self.location = new_location

    def __repr__(self):
        return f"{self.location}'daki {self.color} renkli {self.type}"


at1 = Piece((0, 1), PieceType.KNIGHT, PieceColor.WHITE)
at2 =  Piece((0, 6), PieceType.KNIGHT, PieceColor.WHITE)




tahta = [[at1, at2]]


print(tahta[-1])

print("*"*50)


son_durum = deepcopy(tahta[-1])


son_durum[0].set_location((3,1))

tahta.append(son_durum)

print(tahta)


