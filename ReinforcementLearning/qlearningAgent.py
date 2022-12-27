from copy import deepcopy
from agent import Agent
from utils import Piece, Player, Counter
import random
from data import EvaluationMatrix


class QLearningAgent(Agent,EvaluationMatrix):
    def __init__(self, direction: Player,alpha=0.2, gamma=0.8, epsilon=0, q_value=None):
        """
        alpha    - learning rate
        gamma    - discount factor
        numTraining - number of training episodes
        """
        super().__init__(direction)
        EvaluationMatrix.__init__(self)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)
        self.q_value = q_value
        self.last_state = None
        self.last_action=None
        self.playerSide = direction
        self.myreward=0

    def getQValueBoard(self) -> Counter:
        return self.q_value

    def getQValue(self, current_board, action: tuple[tuple[int, int], tuple[int, int]]) -> float:

        return self.q_value[(current_board, action)]

    def computeActionFromQValues(self, current_board) -> tuple[tuple[int, int], tuple[int, int]]:
        q_list = [self.getQValue(current_board, action) for action in self.game.getLegalActionsBySide(self.direction)]
        max_q = max(q_list)
        max_index = []
        for i in range(len(q_list)):
            if q_list[i] == max_q:
                max_index.append(i)
        index = random.choice(max_index)
        return self.game.getLegalActionsBySide(self.direction)[index]


    def update(self, current_action):
        # get the old estimate
        old_estimate = self.getQValue(self.last_state, self.last_action)
        # compute max Q
        best_action=self.computeActionFromQValues(self.game)
        max_q = self.getQValue(self.game, best_action)
        opponentReward=self.getReward(self.game.getGameState(),current_action,Player.reverse(self.playerSide))
        reward=self.myreward-opponentReward
        sample = reward + self.discount * max_q
        # update the q_value
        self.q_value[(self.last_state, self.last_action)] = (1 - self.alpha) * old_estimate + self.alpha * sample

    def getReward(self, state, action: tuple[tuple[int, int], tuple[int, int]], direction) -> float:
        """
            If the action has eaten one piece, return the corresponding reward;
            Else 0
        """
        score = 0
        nextstate=state.getNextState(action)
        nextstate.swapDirection()
        winner = nextstate.getWinner()
        if winner == direction:
            score = 100000
        elif winner == Player.reverse(direction):
            score =  -100000
        else:
            myPiece = state.getSide(direction)
            for piece in myPiece:
                x, y = piece
                pieceType = state[x][y]
                score += self.pieceValue[pieceType] * self.pieceScore[pieceType][x][y]
            eatenPieceType = self.game.board[action[1][0]][action[1][1]]
            if eatenPieceType == Piece.BSoldier or eatenPieceType == Piece.RSoldier:
                score += 1
            elif eatenPieceType == Piece.BAdvisor or eatenPieceType == Piece.RAdvisor:
                score += 2
            elif eatenPieceType == Piece.BElephant or eatenPieceType == Piece.RElephant:
                score += 2
            elif eatenPieceType == Piece.BHorse or eatenPieceType == Piece.RHorse:
                score += 4
            elif eatenPieceType == Piece.BCannon or eatenPieceType == Piece.RCannon:
                score += 4.5
            elif eatenPieceType == Piece.BChariot or eatenPieceType == Piece.RChariot:
                score += 9
        return score
        

    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
        # get action
        action = self.computeActionFromQValues(self.game.getGameState())
        # save action and state
        self.last_action=action
        self.last_state=self.game.getGameState()
        # get reward
        self.myreward = self.getReward(self.last_state,self.last_action,self.playerSide)
        return action
