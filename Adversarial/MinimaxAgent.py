from agent import Agent
from data import EvaluationMatrix
from utils import Player
import math
from gameModel import GameState


class MinimaxAgent(Agent, EvaluationMatrix):

    def __init__(self, direction: Player, depth=2):
        Agent.__init__(self, direction)
        EvaluationMatrix.__init__(self)
        self.index = 0
        self.depth = depth
        self.playerSide = direction

    def evaluationFunction(self, gameState: GameState) -> int:
        gameState.swapDirection()
        winner = gameState.getWinner()
        gameState.swapDirection()
        if winner == self.playerSide:
            return 1000000
        elif winner == Player.reverse(self.playerSide):
            return -1000000
        myPiece = gameState.getSide(self.playerSide)
        enemyPiece = gameState.getSide(Player.reverse(self.playerSide))
        myThreat = gameState.getThreatBySide(self.playerSide)
        myScore = 0
        enemyScore = 0
        for piece in myPiece:
            x, y = piece
            pieceType = gameState[x][y]
            myScore += self.pieceValue[pieceType] * self.pieceScore[pieceType][x][y]
            attackPosition = gameState.getRange(piece)
            for position in attackPosition:
                x, y = position
                pieceType = gameState[x][y]
                myScore += self.pieceValue[pieceType]
            for threat in myThreat[piece]:
                x, y = threat
                pieceType = gameState[x][y]
                myScore -= self.pieceValue[pieceType]
        for piece in enemyPiece:
            x, y = piece
            pieceType = gameState[x][y]
            enemyScore += self.pieceValue[pieceType] * self.pieceScore[pieceType][x][y]
        return myScore - enemyScore

    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:

        def maxValue(state, depth, playerSide, a, b):
            if depth == self.depth * 2 or state.isMatchOver():
                return self.evaluationFunction(state)
            maximum = -math.inf
            legalActions = state.getLegalActionsBySide(playerSide)
            for action in legalActions:
                maximum = max(maximum,
                              minValue(state.getNextState(action), depth + 1, Player.reverse(playerSide), a, b))
                if maximum > b:
                    return maximum
                a = max(a, maximum)
            return maximum

        def minValue(state, depth, playerSide, a, b):
            if depth == self.depth * 2 or state.isMatchOver():
                return self.evaluationFunction(state)
            minimum = math.inf
            legalActions = state.getLegalActionsBySide(playerSide)
            for action in legalActions:
                minimum = min(minimum,
                              maxValue(state.getNextState(action), depth + 1, Player.reverse(playerSide), a, b))
                if minimum < a:
                    return minimum
                b = min(b, minimum)
            return minimum

        print("Minimax Agent is thinking...")
        gameState = self.game.getGameState()
        legalMoves = gameState.getLegalActionsBySide(self.playerSide)
        bestMove = None
        bestValue = -math.inf
        alpha = -math.inf
        beta = math.inf
        for move in legalMoves:
            value = minValue(gameState.getNextState(move), 1, Player.reverse(self.playerSide), alpha, beta)
            if value > bestValue:
                bestValue = value
                bestMove = move
            if value > beta:
                break
            alpha = max(alpha, value)
        print("Minimax Agent has finished thinking...")
        return bestMove
