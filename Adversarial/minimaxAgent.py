from abc import ABC
from typing import Optional

from agent import Agent
from utils import Piece, Player
import math
import copy


class minimaxAgent(Agent):

    def __init__(self, direction: Player, depth: int):
        super().__init__(direction)
        self.index = 0
        self.depth = depth
        self.playerSide = direction

    def getLegalMoves(self, agentIndex) -> list[tuple[tuple[int, int], tuple[int, int]]]:

        allPieces = self.game.getSide(self.playerSide)
        legalMoves = []
        for piecePosition in allPieces:
            for targetPosition in self.game.getRange(piecePosition):
                if self.game.isValidMove(piecePosition, targetPosition):
                    legalMoves.append((piecePosition, targetPosition))
        return legalMoves

    def evaluationFunction(self):
        return 0

    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:

        def maxValue(state, depth, agentIndex, alpha, beta):
            if depth == self.depth * 2:
                return self.evaluationFunction()
            value = -math.inf
            legalMoves = self.getLegalMoves(agentIndex)
            for action in legalMoves:
                value = max(value, minValue(depth + 1, agentIndex ^ 1, alpha, beta))
                if value > beta:
                    return value
                alpha = max(alpha, value)
            return value

        def minValue(state, depth, agentIndex, alpha, beta):
            if depth == self.depth * 2:
                return self.evaluationFunction()
            value = math.inf
            legalMoves = self.getLegalMoves()
            for action in legalMoves:
                value = min(value, maxValue(depth + 1, agentIndex ^ 1, alpha, beta))
                if value < alpha:
                    return value
                beta = min(beta, value)
            return value