from abc import ABC, abstractmethod

from gameModel import GameModel


class Agent(ABC):
    def __init__(self, direction: bool):
        self.game = None
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
    # 1. TODO: doc
    #
    # The following functions / statement may be helpful for your decision:
    # 1.
    #
    @abstractmethod
    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
        raise NotImplementedError
