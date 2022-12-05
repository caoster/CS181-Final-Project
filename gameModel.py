from typing import Final

from utils import Piece
from gameView import GameView


class GameModel:
    RED: Final[bool] = True
    BLACK: Final[bool] = False

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
        self.direction = GameModel.RED
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
            return 0 <= loc_x <= 9 and 0 <= loc_y <= 10

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
            if position == (3, 0):
                checkForBlack(3, 1)
                checkForBlack(4, 0)
            elif position == (3, 1):
                checkForBlack(3, 0)
                checkForBlack(4, 1)
                checkForBlack(3, 2)
            elif position == (3, 2):
                checkForBlack(3, 1)
                checkForBlack(4, 2)
            elif position == (4, 0):
                checkForBlack(3, 0)
                checkForBlack(4, 2)
                checkForBlack(5, 0)
            elif position == (4, 1):
                checkForBlack(3, 1)
                checkForBlack(4, 0)
                checkForBlack(4, 2)
                checkForBlack(6, 1)
            elif position == (4, 2):
                checkForBlack(4, 1)
                checkForBlack(3, 2)
                checkForBlack(5, 2)
            elif position == (5, 0):
                checkForBlack(4, 0)
                checkForBlack(5, 1)
            elif position == (5, 1):
                checkForBlack(5, 0)
                checkForBlack(4, 1)
                checkForBlack(5, 2)
            elif position == (5, 2):
                checkForBlack(5, 1)
                checkForBlack(4, 2)

        elif pieceType == Piece.BAdvisor:  # 2
            if position == (3, 0):
                checkForBlack(4, 1)
            elif position == (5, 0):
                checkForBlack(4, 1)
            elif position == (3, 2):
                checkForBlack(4, 1)
            elif position == (5, 2):
                checkForBlack(4, 1)
            elif position == (4, 1):
                checkForBlack(3, 0)
                checkForBlack(5, 0)
                checkForBlack(3, 2)
                checkForBlack(5, 2)

        elif pieceType == Piece.BElephant:  # 3
            if inRange(x - 1, y - 1) and checkEmpty(x - 1, y - 1) and 0 <= y - 2 <= 4:
                safeCheckForBlack(x - 2, y - 2)
            if inRange(x + 1, y - 1) and checkEmpty(x + 1, y - 1) and 0 <= y - 2 <= 4:
                safeCheckForBlack(x + 2, y - 2)
            if inRange(x - 1, y + 1) and checkEmpty(x - 1, y + 1) and 0 <= y + 2 <= 4:
                safeCheckForBlack(x - 2, y + 2)
            if inRange(x + 1, y + 1) and checkEmpty(x + 1, y + 1) and 0 <= y + 2 <= 4:
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
            # Direction: right
            for i in range(10):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                checkForBlack(x + i, y)
                break
            # Direction: left
            for i in range(10):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                checkForBlack(x - i, y)
                break
            # Direction: up
            for i in range(10):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                checkForBlack(x, y - i)
                break
            # Direction: down
            for i in range(10):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                checkForBlack(x, y + i)
                break

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
            # Direction: left
            for i in range(10):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x - j, y):
                        break
                    if not checkEmpty(x - j, y):
                        if Piece.getSide(self.board[x - j][y]) == 1:
                            result.append((x - j, y))
                        break
                break
            # Direction: up
            for i in range(10):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x, y - j):
                        break
                    if not checkEmpty(x, y - j):
                        if Piece.getSide(self.board[x][y - j]) == 1:
                            result.append((x, y - j))
                        break
                break
            # Direction: down
            for i in range(10):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x, y + j):
                        break
                    if not checkEmpty(x, y + j):
                        if Piece.getSide(self.board[x][y + j]) == 1:
                            result.append((x, y + j))
                        break
                break

        elif pieceType == Piece.BSoldier:  # 7
            if y <= 4:
                checkForBlack(x, y + 1)
            else:
                safeCheckForBlack(x, y + 1)
                safeCheckForBlack(x - 1, y)
                safeCheckForBlack(x + 1, y)

        elif pieceType == Piece.RGeneral:  # 8
            if position == (3, 9):
                checkForRed(3, 8)
                checkForRed(4, 9)
            elif position == (4, 9):
                checkForRed(3, 9)
                checkForRed(5, 9)
                checkForRed(4, 8)
            elif position == (5, 9):
                checkForRed(4, 9)
                checkForRed(5, 8)
            elif position == (3, 8):
                checkForRed(3, 7)
                checkForRed(4, 8)
                checkForRed(3, 9)
            elif position == (4, 8):
                checkForRed(3, 8)
                checkForRed(4, 9)
                checkForRed(5, 8)
                checkForRed(4, 7)
            elif position == (5, 8):
                checkForRed(4, 8)
                checkForRed(5, 7)
                checkForRed(5, 9)
            elif position == (3, 7):
                checkForRed(3, 8)
                checkForRed(4, 7)
            elif position == (4, 7):
                checkForRed(3, 7)
                checkForRed(4, 8)
                checkForRed(5, 7)
            elif position == (5, 7):
                checkForRed(4, 7)
                checkForRed(5, 8)

        elif pieceType == Piece.RAdvisor:  # 9
            if position == (3, 9):
                checkForRed(4, 8)
            elif position == (3, 7):
                checkForRed(4, 8)
            elif position == (5, 7):
                checkForRed(4, 8)
            elif position == (5, 9):
                checkForRed(4, 8)
            elif position == (4, 8):
                checkForRed(3, 7)
                checkForRed(3, 9)
                checkForRed(5, 7)
                checkForRed(5, 9)

        elif pieceType == Piece.RElephant:  # 10
            if inRange(x - 1, y - 1) and checkEmpty(x - 1, y - 1) and 5 <= y - 2 <= 9:
                checkForRed(x - 2, y - 2)
            if inRange(x + 1, y - 1) and checkEmpty(x + 1, y - 1) and 5 <= y - 2 <= 9:
                checkForRed(x + 2, y - 2)
            if inRange(x - 1, y + 1) and checkEmpty(x - 1, y + 1) and 5 <= y + 2 <= 9:
                checkForRed(x - 2, y + 2)
            if inRange(x + 1, y + 1) and checkEmpty(x + 1, y + 1) and 5 <= y + 2 <= 9:
                checkForRed(x + 2, y + 2)

        elif pieceType == Piece.RHorse:  # 11
            if inRange(x + 1, y) and checkEmpty(x + 1, y):
                checkForRed(x + 2, y - 1)
                checkForRed(x + 2, y + 1)
            if inRange(x, y + 1) and checkEmpty(x, y + 1):
                checkForRed(x + 1, y + 2)
                checkForRed(x - 1, y + 2)
            if inRange(x - 1, y) and checkEmpty(x - 1, y):
                checkForRed(x - 2, y + 1)
                checkForRed(x - 2, y - 1)
            if inRange(x, y - 1) and checkEmpty(x, y - 1):
                checkForRed(x - 1, y - 2)
                checkForRed(x + 1, y - 2)

        elif pieceType == Piece.RChariot:  # 12
            # Direction: right
            for i in range(10):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                checkForRed(x + i, y)
                break
            # Direction: left
            for i in range(10):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                checkForRed(x - i, y)
                break
            # Direction: up
            for i in range(10):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                checkForRed(x, y - i)
                break
            # Direction: down
            for i in range(10):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                checkForRed(x, y + i)
                break

        elif pieceType == Piece.RCannon:  # 13
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
                        if Piece.getSide(self.board[x + j][y]) == -1:
                            result.append((x + j, y))
                        break
                break
            # Direction: left
            for i in range(10):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x - j, y):
                        break
                    if not checkEmpty(x - j, y):
                        if Piece.getSide(self.board[x - j][y]) == -1:
                            result.append((x - j, y))
                        break
                break
            # Direction: up
            for i in range(10):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x, y - j):
                        break
                    if not checkEmpty(x, y - j):
                        if Piece.getSide(self.board[x][y - j]) == -1:
                            result.append((x, y - j))
                        break
                break
            # Direction: down
            for i in range(10):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x, y + j):
                        break
                    if not checkEmpty(x, y + j):
                        if Piece.getSide(self.board[x][y + j]) == -1:
                            result.append((x, y + j))
                        break
                break

        elif pieceType == Piece.RSoldier:  # 14
            if y >= 5:
                checkForRed(x, y - 1)
            else:
                safeCheckForRed(x, y - 1)
                safeCheckForRed(x - 1, y)
                safeCheckForRed(x + 1, y)

        return result

    def getSide(self, side: bool) -> list[tuple[int, int]]:
        v = -1  # Black
        if side:
            v = 1  # Red
        result = []
        for i, x in enumerate(self.board):
            result += [(i, j) for j, y in enumerate(x) if Piece.getSide(y) == v]
        return result

    def startGame(self):
        # TODO: Call two agents
        while True:
            # Some agent
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
            self.direction = not self.direction
        pass

    def _matchOver(self) -> int:
        # return 0 for not over
        # return 1 for Red winning
        # return 2 for Black winning
        # return 3 for draw(?)
        justMoved = self.direction
        if not any(Piece.BGeneral in i for i in self.board):
            return 1
        elif not any(Piece.RGeneral in i for i in self.board):
            return 2

        # TODO: Flying General

        redLose = True
        all_red = self.getSide(GameModel.RED)
        for redPiece in all_red:
            if self.getRange(redPiece):
                redLose = False
                break
        if redLose:
            return 1

        blackLose = True
        all_black = self.getSide(GameModel.BLACK)
        for blackPiece in all_black:
            if self.getRange(blackPiece):
                blackLose = True
                break
        if blackLose:
            return 2

        return 0

    def _draw(self) -> None:
        self.canvas.draw(self.board)

    def startApp(self) -> None:
        self.canvas.startApp()
