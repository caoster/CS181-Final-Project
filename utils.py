import enum


class Player(enum.Enum):
    NoneType = 0
    Red = 1
    Black = -1

    @staticmethod
    def reverse(side):
        if side == Player.NoneType:
            return Player.NoneType
        elif side == Player.Red:
            return Player.Black
        else:
            return Player.Red


class Piece(enum.Enum):
    # Black/Red
    # General, Advisor, Elephant, Horse, Chariot, Cannon, Soldier
    NoneType = 0
    BGeneral = 1
    BAdvisor = 2
    BElephant = 3
    BHorse = 4
    BChariot = 5
    BCannon = 6
    BSoldier = 7
    RGeneral = 8
    RAdvisor = 9
    RElephant = 10
    RHorse = 11
    RChariot = 12
    RCannon = 13
    RSoldier = 14

    @staticmethod
    def getSide(piece) -> Player:
        if piece == Piece.NoneType:
            return Player.NoneType
        elif "R" == piece.name[0]:
            return Player.Red
        else:
            return Player.Black

    def __str__(self):
        return self.name
