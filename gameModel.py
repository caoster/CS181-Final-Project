import time

from utils import Piece, Player
from gameView import GameView


class GameModel:

    def __init__(self, canvas: GameView, RedAgent, BlackAgent, interval: float):
        self._board = [
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
        self._interval: float = interval
        self._canvas: GameView = canvas
        self._canvas.setModel(self)
        self._direction: Player = Player.Red
        self._red_agent = RedAgent
        self._red_agent.setGameModel(self)
        self._black_agent = BlackAgent
        self._black_agent.setGameModel(self)
        self._draw()

    # Note that this function do not care which side you are
    def isValidMove(self, src: tuple[int, int], dst: tuple[int, int]) -> bool:
        src_x, src_y = src
        piece = self._board[src_x][src_y]
        if piece == Piece.NoneType:
            return False
        return dst in self.getRange(src)

    # Make attribute board read-only to agent
    @property
    def board(self):
        return self._board

    # Don't try to modify this function: it is strange and ugly but fully tested in CS132!
    def getRange(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = position
        pieceType = self._board[x][y]
        result: list[tuple[int, int]] = []
        if pieceType == Piece.NoneType:
            return result

        def checkEmpty(loc_x, loc_y):
            return self._board[loc_x][loc_y] == Piece.NoneType

        def inRangeAndEmpty(loc_x, loc_y):
            if inRange(loc_x, loc_y):
                return self._board[loc_x][loc_y] == Piece.NoneType
            return False

        def inRange(loc_x, loc_y):
            return 0 <= loc_x < 9 and 0 <= loc_y < 10

        def checkForBlack(loc_x, loc_y):
            if Piece.getSide(self._board[loc_x][loc_y]) != Player.Black:
                result.append((loc_x, loc_y))

        def checkForRed(loc_x, loc_y):
            if Piece.getSide(self._board[loc_x][loc_y]) != Player.Red:
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
                checkForBlack(4, 1)
                checkForBlack(5, 0)
            elif position == (4, 1):
                checkForBlack(3, 1)
                checkForBlack(4, 0)
                checkForBlack(4, 2)
                checkForBlack(5, 1)
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
            if inRangeAndEmpty(x - 1, y - 1) and 0 <= y - 2 <= 4:
                safeCheckForBlack(x - 2, y - 2)
            if inRangeAndEmpty(x + 1, y - 1) and 0 <= y - 2 <= 4:
                safeCheckForBlack(x + 2, y - 2)
            if inRangeAndEmpty(x - 1, y + 1) and 0 <= y + 2 <= 4:
                safeCheckForBlack(x - 2, y + 2)
            if inRangeAndEmpty(x + 1, y + 1) and 0 <= y + 2 <= 4:
                safeCheckForBlack(x + 2, y + 2)

        elif pieceType == Piece.BHorse:  # 4
            if inRangeAndEmpty(x + 1, y):
                safeCheckForBlack(x + 2, y - 1)
                safeCheckForBlack(x + 2, y + 1)
            if inRangeAndEmpty(x, y + 1):
                safeCheckForBlack(x + 1, y + 2)
                safeCheckForBlack(x - 1, y + 2)
            if inRangeAndEmpty(x - 1, y):
                safeCheckForBlack(x - 2, y + 1)
                safeCheckForBlack(x - 2, y - 1)
            if inRangeAndEmpty(x, y - 1):
                safeCheckForBlack(x - 1, y - 2)
                safeCheckForBlack(x + 1, y - 2)

        elif pieceType == Piece.BChariot:  # 5
            # Direction: right
            for i in range(1, 10):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                checkForBlack(x + i, y)
                break
            # Direction: left
            for i in range(1, 10):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                checkForBlack(x - i, y)
                break
            # Direction: up
            for i in range(1, 10):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                checkForBlack(x, y - i)
                break
            # Direction: down
            for i in range(1, 10):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                checkForBlack(x, y + i)
                break

        elif pieceType == Piece.BCannon:  # 6
            # Direction: right
            for i in range(1, 10):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x + j, y):
                        break
                    if not checkEmpty(x + j, y):
                        if Piece.getSide(self._board[x + j][y]) == Player.Red:
                            result.append((x + j, y))
                        break
                break
            # Direction: left
            for i in range(1, 10):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x - j, y):
                        break
                    if not checkEmpty(x - j, y):
                        if Piece.getSide(self._board[x - j][y]) == Player.Red:
                            result.append((x - j, y))
                        break
                break
            # Direction: up
            for i in range(1, 10):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x, y - j):
                        break
                    if not checkEmpty(x, y - j):
                        if Piece.getSide(self._board[x][y - j]) == Player.Red:
                            result.append((x, y - j))
                        break
                break
            # Direction: down
            for i in range(1, 10):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x, y + j):
                        break
                    if not checkEmpty(x, y + j):
                        if Piece.getSide(self._board[x][y + j]) == Player.Red:
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
            if inRangeAndEmpty(x - 1, y - 1) and 5 <= y - 2 <= 9:
                safeCheckForRed(x - 2, y - 2)
            if inRangeAndEmpty(x + 1, y - 1) and 5 <= y - 2 <= 9:
                safeCheckForRed(x + 2, y - 2)
            if inRangeAndEmpty(x - 1, y + 1) and 5 <= y + 2 <= 9:
                safeCheckForRed(x - 2, y + 2)
            if inRangeAndEmpty(x + 1, y + 1) and 5 <= y + 2 <= 9:
                safeCheckForRed(x + 2, y + 2)

        elif pieceType == Piece.RHorse:  # 11
            if inRangeAndEmpty(x + 1, y):
                safeCheckForRed(x + 2, y - 1)
                safeCheckForRed(x + 2, y + 1)
            if inRangeAndEmpty(x, y + 1):
                safeCheckForRed(x + 1, y + 2)
                safeCheckForRed(x - 1, y + 2)
            if inRangeAndEmpty(x - 1, y):
                safeCheckForRed(x - 2, y + 1)
                safeCheckForRed(x - 2, y - 1)
            if inRangeAndEmpty(x, y - 1):
                safeCheckForRed(x - 1, y - 2)
                safeCheckForRed(x + 1, y - 2)

        elif pieceType == Piece.RChariot:  # 12
            # Direction: right
            for i in range(1, 10):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                checkForRed(x + i, y)
                break
            # Direction: left
            for i in range(1, 10):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                checkForRed(x - i, y)
                break
            # Direction: up
            for i in range(1, 10):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                checkForRed(x, y - i)
                break
            # Direction: down
            for i in range(1, 10):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                checkForRed(x, y + i)
                break

        elif pieceType == Piece.RCannon:  # 13
            # Direction: right
            for i in range(1, 10):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x + j, y):
                        break
                    if not checkEmpty(x + j, y):
                        if Piece.getSide(self._board[x + j][y]) == Player.Black:
                            result.append((x + j, y))
                        break
                break
            # Direction: left
            for i in range(1, 10):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x - j, y):
                        break
                    if not checkEmpty(x - j, y):
                        if Piece.getSide(self._board[x - j][y]) == Player.Black:
                            result.append((x - j, y))
                        break
                break
            # Direction: up
            for i in range(1, 10):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x, y - j):
                        break
                    if not checkEmpty(x, y - j):
                        if Piece.getSide(self._board[x][y - j]) == Player.Black:
                            result.append((x, y - j))
                        break
                break
            # Direction: down
            for i in range(1, 10):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x, y + j):
                        break
                    if not checkEmpty(x, y + j):
                        if Piece.getSide(self._board[x][y + j]) == Player.Black:
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

    def getSide(self, side: Player) -> list[tuple[int, int]]:
        return self._find_all_position_that_satisfies(lambda a: Piece.getSide(a) == side)

    # Return all locations of this kind of piece
    def findPiece(self, piece: Piece) -> list[tuple[int, int]]:
        return self._find_all_position_that_satisfies(lambda a: a == piece)

    def startGame(self):
        time.sleep(1)  # Always sleep one second before initiating
        while True:
            if self._direction == Player.Red:
                src, dst = self._red_agent.step()
            elif self._direction == Player.Black:
                src, dst = self._black_agent.step()
            else:
                raise  # Robustness
            if not self.isValidMove(src, dst):
                print("Invalid move!")
                break
            if Piece.getSide(self._board[src[0]][src[1]]) != self._direction:
                print("You should only move your own piece!")
                break
            self._board[dst[0]][dst[1]] = self._board[src[0]][src[1]]
            self._board[src[0]][src[1]] = Piece.NoneType

            self._draw()
            time.sleep(self._interval)

            result = self._matchOver()
            self._direction = Player.reverse(self._direction)
            if result == Player.NoneType:
                continue
            elif result == Player.Red:
                print("Red win!")
                break
                # Red wins
            elif result == Player.Black:
                print("Black win!")
                break
                # Black wins
            else:
                print("Draw!")
                break
                # Draw?
        pass

    def _matchOver(self) -> Player:
        if not any(Piece.BGeneral in i for i in self._board):
            return Player.Red  # BlackGeneral captured, Red wins
        elif not any(Piece.RGeneral in i for i in self._board):
            return Player.Black  # RedGeneral captured, Black wins

        justMoved = self._direction
        redG_x, redG_y = self.findPiece(Piece.RGeneral)[0]
        blackG_x, blackG_y = self.findPiece(Piece.BGeneral)[0]
        if redG_x == blackG_x:
            fly = True
            for i in range(blackG_y + 1, redG_y):
                if Piece.getSide(self._board[redG_x][i]) != Player.NoneType:
                    fly = False
                    break
            if fly:
                if justMoved == Player.Red:
                    return Player.Black  # Black wins
                else:
                    return Player.Red  # Red wins

        redLose = True
        all_red = self.getSide(Player.Red)
        for redPiece in all_red:
            if self.getRange(redPiece):
                redLose = False
                break
        if redLose:
            return Player.Black

        blackLose = True
        all_black = self.getSide(Player.Black)
        for blackPiece in all_black:
            if self.getRange(blackPiece):
                blackLose = False
                break
        if blackLose:
            return Player.Red

        return Player.NoneType

    def _draw(self) -> None:
        self._canvas.draw(self._board)

    def _find_all_position_that_satisfies(self, condition: callable) -> list[tuple[int, int]]:
        result = []
        for i, x in enumerate(self._board):
            result += [(i, j) for j, y in enumerate(x) if condition(y)]
        return result

    def startApp(self) -> None:
        self.startGame()
        self._canvas.startApp()
