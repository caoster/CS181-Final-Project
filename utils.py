import enum


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

    # 0  for NoneType
    # 1  for Red
    # -1 for Black
    @staticmethod
    def getSide(piece) -> int:
        if piece == Piece.NoneType:
            return 0
        elif "R" == piece.name[0]:
            return 1
        else:
            return -1

    # Return False iff piece1 and piece2 are both Red or both Black
    @staticmethod
    def diffSideOrEmpty(piece1, piece2) -> int:
        return Piece.getSide(piece1) * Piece.getSide(piece2) != 1
