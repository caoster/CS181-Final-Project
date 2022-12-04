from utils import Piece
from gameView import GameView


class GameModel:
    def __init__(self, canvas: GameView):
        self.board = [
            [Piece.BChariot, Piece.NoneType, Piece.NoneType, Piece.BSoldier, Piece.NoneType, Piece.NoneType, Piece.RSoldier, Piece.NoneType, Piece.NoneType, Piece.RChariot],
            [Piece.BHorse, Piece.NoneType, Piece.BCannon, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.RCannon, Piece.NoneType, Piece.RHorse],
            [Piece.BElephant, Piece.NoneType, Piece.NoneType, Piece.BSoldier, Piece.NoneType, Piece.NoneType, Piece.RSoldier, Piece.NoneType, Piece.NoneType, Piece.RElephant],
            [Piece.BAdvisor, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.RAdvisor],
            [Piece.BGeneral, Piece.NoneType, Piece.NoneType, Piece.BSoldier, Piece.NoneType, Piece.NoneType, Piece.RSoldier, Piece.NoneType, Piece.NoneType, Piece.RGeneral],
            [Piece.BAdvisor, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.RAdvisor],
            [Piece.BElephant, Piece.NoneType, Piece.NoneType, Piece.BSoldier, Piece.NoneType, Piece.NoneType, Piece.RSoldier, Piece.NoneType, Piece.NoneType, Piece.RElephant],
            [Piece.BHorse, Piece.NoneType, Piece.BCannon, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.RCannon, Piece.NoneType, Piece.RHorse],
            [Piece.BChariot, Piece.NoneType, Piece.NoneType, Piece.BSoldier, Piece.NoneType, Piece.NoneType, Piece.RSoldier, Piece.NoneType, Piece.NoneType, Piece.RChariot]
        ]
        self.canvas = canvas
        self.canvas.setModel(self)
        self.direction = True  # True for Red, False for Black
        self._draw()

    def isValidMove(self, src: tuple[int, int], dst: tuple[int, int]) -> bool:
        src_x, src_y = src
        piece = self.board[src_x][src_y]
        assert piece != Piece.NoneType, print("You shall not move a NoneType piece!")
        return dst in self.getRange(src)

    # Don't try to modify this function: it is strange and ugly but fully tested in CS132!
    # TODO: declare this function out of the file
    def getRange(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = position
        pieceType = self.board[x][y]
        result: list[tuple[int, int]] = []
        if pieceType == Piece.NoneType:
            return result

        def checkEmpty(loc_x, loc_y):
            return self.board[loc_x][loc_y] == Piece.NoneType

        def inRange(loc_x, loc_y):
            return 0 < loc_x < 10 and 0 < loc_y < 11

        def checkForBlack(loc_x, loc_y):
            if Piece.getSide(self.board[loc_x][loc_y]) != -1:
                result.append((loc_x, loc_y))

        def checkForRed(loc_x, loc_y):
            if Piece.getSide(self.board[loc_x][loc_y]) != 1:
                result.append((loc_x, loc_y))

        def safeCheckForBlack(loc_x, loc_y):
            if inRange(loc_x, loc_y):
                checkForBlack(loc_x, loc_y)

        def safeCheckForRed(loc_x, loc_y):
            if inRange(loc_x, loc_y):
                checkForRed(loc_x, loc_y)

        if pieceType == Piece.BGeneral:  # 1
            if position == (4, 1):
                checkForBlack(4, 2)
                checkForBlack(5, 1)
            elif position == (4, 2):
                checkForBlack(4, 1)
                checkForBlack(5, 2)
                checkForBlack(4, 3)
            elif position == (4, 3):
                checkForBlack(4, 2)
                checkForBlack(5, 3)
            elif position == (5, 1):
                checkForBlack(4, 1)
                checkForBlack(5, 2)
                checkForBlack(6, 1)
            elif position == (5, 2):
                checkForBlack(4, 2)
                checkForBlack(5, 1)
                checkForBlack(5, 3)
                checkForBlack(6, 2)
            elif position == (5, 3):
                checkForBlack(5, 2)
                checkForBlack(4, 3)
                checkForBlack(6, 3)
            elif position == (6, 1):
                checkForBlack(5, 1)
                checkForBlack(6, 2)
            elif position == (6, 2):
                checkForBlack(6, 1)
                checkForBlack(5, 2)
                checkForBlack(6, 3)
            elif position == (6, 3):
                checkForBlack(6, 2)
                checkForBlack(5, 3)

        elif pieceType == Piece.BAdvisor:  # 2
            if position == (4, 1):
                checkForBlack(5, 2)
            elif position == (6, 1):
                checkForBlack(5, 2)
            elif position == (4, 3):
                checkForBlack(5, 2)
            elif position == (6, 3):
                checkForBlack(5, 2)
            elif position == (5, 2):
                checkForBlack(4, 1)
                checkForBlack(6, 1)
                checkForBlack(4, 3)
                checkForBlack(6, 3)

        elif pieceType == Piece.BElephant:  # 3
            if inRange(x - 1, y - 1) and checkEmpty(x - 1, y - 1) and 0 < y - 2 < 5:
                safeCheckForBlack(x - 2, y - 2)
            if inRange(x + 1, y - 1) and checkEmpty(x + 1, y - 1) and 0 < y - 2 < 5:
                safeCheckForBlack(x + 2, y - 2)
            if inRange(x - 1, y + 1) and checkEmpty(x - 1, y + 1) and 0 < y + 2 < 5:
                safeCheckForBlack(x - 2, y + 2)
            if inRange(x + 1, y + 1) and checkEmpty(x + 1, y + 1) and 0 < y + 2 < 5:
                safeCheckForBlack(x + 2, y + 2)

        elif pieceType == Piece.BHorse:  # 4
            if inRange(x + 1, y) and checkEmpty(x + 1, y):
                safeCheckForBlack(x + 2, y - 1)
                safeCheckForBlack(x + 2, y + 1)
            if inRange(x, y + 1) and checkEmpty(x, y + 1):
                safeCheckForBlack(x + 1, y + 2)
                safeCheckForBlack(x - 1, y + 2)
            if inRange(x - 1, y) and checkEmpty(x - 1, y):
                safeCheckForBlack(x - 2, y + 1)
                safeCheckForBlack(x - 2, y - 1)
            if inRange(x, y - 1) and checkEmpty(x, y - 1):
                safeCheckForBlack(x - 1, y - 2)
                safeCheckForBlack(x + 1, y - 2)

        elif pieceType == Piece.BChariot:  # 5
            # TODO: here
            pass

        elif pieceType == Piece.BCannon:  # 6
            # Direction: right
            for i in range(10):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x + j, y):
                        break
                    if not checkEmpty(x + j, y):
                        if Piece.getSide(self.board[x + j][y]) == 1:
                            result.append((x + j, y))
                        break
                break
            # TODO: here

        elif pieceType == Piece.BSoldier:  # 7
            pass
        elif pieceType == Piece.RGeneral:  # 8
            pass
        elif pieceType == Piece.RAdvisor:  # 9
            pass
        elif pieceType == Piece.RElephant:  # 10
            pass
        elif pieceType == Piece.RHorse:  # 11
            pass
        elif pieceType == Piece.RChariot:  # 12
            pass
        elif pieceType == Piece.RCannon:  # 13
            pass
        elif pieceType == Piece.RSoldier:  # 14
            pass

        return result

    def startGame(self):
        # TODO: Call two agents
        while True:
            # Some agent
            self.direction = not self.direction
            result = self._matchOver()
            if result == 0:
                continue
            elif result == 1:
                # Red wins
                pass
            elif result == 2:
                # Black wins
                pass
            else:
                # Draw?
                pass
        pass

    def _matchOver(self) -> int:
        # TODO: helper function: check whether the match is over
        # return 0 for not over
        # return 1 for Red winning
        # return 2 for Black winning
        # return 3 for draw(?)
        pass

    def _draw(self) -> None:
        self.canvas.draw(self.board)

    def startApp(self) -> None:
        self.canvas.startApp()
