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
    def getRange(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = position
        pieceType = self.board[x][y]
        result: list[tuple[int, int]] = []
        if pieceType == Piece.NoneType:
            return result

        def checkForBlack(loc_x, loc_y):
            return Piece.getSide(self.board[loc_x][loc_y]) != -1

        def checkForRed(loc_x, loc_y):
            return Piece.getSide(self.board[loc_x][loc_y]) != 1

        if pieceType == Piece.BGeneral:  # 1
            pass
        elif pieceType == Piece.BAdvisor:  # 2
            pass
        elif pieceType == Piece.BElephant:  # 3
            pass
        elif pieceType == Piece.BHorse:  # 4
            pass
        elif pieceType == Piece.BChariot:  # 5
            pass
        elif pieceType == Piece.BCannon:  # 6
            pass
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
