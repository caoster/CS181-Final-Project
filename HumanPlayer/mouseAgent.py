from queue import Queue
from typing import Optional

from agent import Agent
from utils import Piece, Player


class MouseAgent(Agent):
    def __init__(self, direction: Player):
        super().__init__(direction)
        self.data: Optional[Queue] = None

    def setTunnelIn(self, tunnel: Queue):
        self.data = tunnel

    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
        input()
        while True:
            move: tuple[tuple[int, int], tuple[int, int]] = self.data.get()
            src, dst = move
            if Piece.getSide(src) != self.direction:
                continue
            if self.game.isValidMove(src, dst):
                return move
