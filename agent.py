from abc import ABC, abstractmethod
from typing import Optional

from gameModel import GameModel


class Agent(ABC):
    def __init__(self, direction: bool):
        self.game: Optional[GameModel] = None
        self.direction: bool = direction

    def setGameModel(self, game: GameModel):
        self.game = game

    # When this function is being called, you should return a step in format of:
    # ((src_x, src_y), (dst_x, dst_y))
    # You should:
    # 1. Make sure you only make valid moves on your own piece.
    # 2.
    #
    # The following functions should never be called:
    # 1. startGame()
    # 2. startApp()
    #
    # The following functions / attribute may be helpful for your decision:
    # 1. isValidMove(...)
    # 2. getRange(...)
    # 3. getSide(...)
    # 4. findPiece(...)
    # 5. self.board  # This is read-only
    #
    @abstractmethod
    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
        raise NotImplementedError
