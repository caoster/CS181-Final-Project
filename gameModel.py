from utils import Piece
from gameView import GameView


class GameModel:
    def __init__(self, canvas: GameView):
        self.board = [
            [Piece.BChariot, Piece.BHorse, Piece.BElephant, Piece.BAdvisor, Piece.BGeneral, Piece.BAdvisor, Piece.BElephant, Piece.BHorse, Piece.BChariot],
            [Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType],
            [Piece.NoneType, Piece.BCannon, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.BCannon, Piece.NoneType],
            [Piece.BSoldier, Piece.NoneType, Piece.BSoldier, Piece.NoneType, Piece.BSoldier, Piece.NoneType, Piece.BSoldier, Piece.NoneType, Piece.BSoldier],
            [Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType],
            [Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType],
            [Piece.RSoldier, Piece.NoneType, Piece.RSoldier, Piece.NoneType, Piece.RSoldier, Piece.NoneType, Piece.RSoldier, Piece.NoneType, Piece.RSoldier],
            [Piece.NoneType, Piece.RCannon, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.RCannon, Piece.NoneType],
            [Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType, Piece.NoneType],
            [Piece.RChariot, Piece.RHorse, Piece.RElephant, Piece.RAdvisor, Piece.RGeneral, Piece.RAdvisor, Piece.RElephant, Piece.RHorse, Piece.RChariot]
        ]
        self.canvas = canvas
        self.canvas.setModel(self)
        self.draw()

    def move(self):
        pass

    def draw(self):
        self.canvas.draw(self.board)

    def startApp(self):
        self.canvas.startApp()
