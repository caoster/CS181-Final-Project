from abc import ABC
from typing import Optional

from agent import Agent
from utils import Piece, Player
import math
from gameModel import GameState


class MinimaxAgent(Agent):

    def __init__(self, direction: Player, depth: int):
        super().__init__(direction)
        self.index = 0
        self.depth = depth
        self.playerSide = direction

    def evaluationFunction(self, gameState: GameState) -> int:
        return 0

    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:

        def maxValue(state, depth, playerSide, a, b):
            if depth == self.depth * 2 or state.getWinner():
                return self.evaluationFunction(state)
            maximum = -math.inf
            legalActions = state.getLegalActionsBySide(playerSide)
            for action in legalActions:
                if playerSide == Player.Red:
                    maximum = max(maximum, minValue(state.getNextState(action), depth + 1, Player.Black, a, b))
                else:
                    maximum = max(maximum, minValue(state.getNextState(action), depth + 1, Player.Red, a, b))
                if value > beta:
                    return value
                a = max(a, maximum)
            return maximum

        def minValue(state, depth, playerSide, a, b):
            if depth == self.depth * 2 or state.getWinner():
                return self.evaluationFunction(state)
            minimum = math.inf
            legalActions = state.getLegalActionsBySide(playerSide)
            for action in legalActions:
                if playerSide == Player.Red:
                    minimum = min(minimum, maxValue(state.getNextState(action), depth + 1, Player.Black, a, b))
                else:
                    minimum = min(minimum, maxValue(state.getNextState(action), depth + 1, Player.Red, a, b))
                if value < a:
                    return value
                b = min(b, minimum)
            return minimum

        gameState = self.game.getGameState()
        legalMoves = gameState.getLegalActionsBySide(self.playerSide)
        bestMove = legalMoves[0]
        bestValue = -math.inf
        alpha = -math.inf
        beta = math.inf
        for move in legalMoves:
            if self.playerSide == Player.Red:
                value = minValue(gameState.getNextState(move), 1, Player.Black, alpha, beta)
            else:
                value = minValue(gameState.getNextState(move), 1, Player.Red, alpha, beta)
            if value > bestValue:
                bestValue = value
                bestMove = move
            if value > beta:
                return bestMove
            alpha = max(alpha, value)
        return bestMove
