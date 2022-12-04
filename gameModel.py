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

    def isValidMove(self, src_x, src_y, dst_x, dst_y) -> bool:
        piece = self.board[src_x][src_y]
        assert piece != Piece.NoneType
        if Piece.diffSideOrEmpty(self.board[src_x][src_y], self.board[dst_x][dst_y]):
            # TODO: check if valid move
            return True
        else:
            return False

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
