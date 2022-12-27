from agent import Agent
from data import EvaluationMatrix
from utils import Player, Piece
import math
from gameModel import GameState


class MinimaxAgent(Agent, EvaluationMatrix):

    def __init__(self, direction: Player, depth=2):
        Agent.__init__(self, direction)
        EvaluationMatrix.__init__(self)
        self.index = 0
        self.depth = depth
        self.playerSide = direction

    def evaluationFunction(self, gameState: GameState) -> float:
        gameState.swapDirection()
        winner = gameState.getWinner()
        gameState.swapDirection()
        if winner == self.playerSide:
            return 1000000
        elif winner == Player.reverse(self.playerSide):
            return -1000000
        myPiece = gameState.getSide(self.playerSide)
        enemyPiece = gameState.getSide(Player.reverse(self.playerSide))
        myScore = 0
        enemyScore = 0
        myThreat = gameState.getThreatBySide(self.playerSide)
        for piece in myPiece:
            x, y = piece
            myPieceType = gameState[x][y]
            myScore += self.pieceValue[myPieceType] * self.pieceScore[myPieceType][x][y]
            myScore *= 0.1

            attackPosition = gameState.getRange(piece)
            flexibility = 0
            for position in attackPosition:
                x, y = position
                pieceType = gameState[x][y]
                if pieceType != Piece.NoneType:
                    myScore += self.pieceValue[pieceType] * 2
                else:
                    flexibility += 1
            myScore += flexibility * self.pieceFlexibility[myPieceType]
            myScore -= self.pieceValue[myPieceType] * len(myThreat[piece])
            protector = gameState.getProtectorBySide(self.playerSide, piece)
            myScore += self.pieceValue[myPieceType] * len(protector)
        for piece in enemyPiece:
            x, y = piece
            pieceType = gameState[x][y]
            enemyScore += self.pieceValue[pieceType] * self.pieceScore[pieceType][x][y]
        return myScore - enemyScore * 0.1

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

        print("Minimax starts thinking...")
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
        print("Minimax stops thinking...")
        return bestMove
