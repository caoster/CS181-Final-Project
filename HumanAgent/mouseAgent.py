from queue import Queue, Empty
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
        print(f"Waiting for {self.direction.name}: ", end=" ")
        try:
            self.data.get(False)  # clear
        except Empty:
            pass
        while True:
            move: tuple[tuple[int, int], tuple[int, int]] = self.data.get()
            src, dst = move
            src_x, src_y = src
            if Piece.getSide(self.game.board[src_x][src_y]) == self.direction:
                if self.game.isValidMove(src, dst):
                    print(" From", src, "To", dst)
                    return move
            print(f"\n{self.direction.name} Invalid move!", end="")
