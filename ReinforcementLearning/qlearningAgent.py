from copy import deepcopy
from typing import Optional
from agent import Agent
from utils import Piece, Player, Counter
from gameModel import GameModel
import random



class QLearningAgent(Agent):
    def __init__(self, direction: Player, numTraining=100, alpha=0.2, gamma=0.8, q_value=None):
        """
        alpha    - learning rate
        gamma    - discount factor
        numTraining - number of training episodes
        """
        super().__init__(direction)

        # self.episodesSoFar = 0
        # self.accumTrainRewards = 0.0
        # self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
        # self.epsilon = float(epsilon)# 好像可以不用
        self.alpha = float(alpha)
        self.discount = float(gamma)
        self.q_value = q_value

    def getQValueBoard(self) -> Counter:
        return self.q_value


    def getQValue(self, current_board, action: tuple[tuple[int, int], tuple[int, int]]) -> float:

        return self.q_value[(current_board,action)]


    # def computeValueFromQValues(self, current_board) -> float:
    #     if self.getLegalActions(current_board)==None:
    #         return None
    #     best_action=self.computeActionFromQValues(current_board)
    #     return self.getQValue(current_board,best_action)
        

    def computeActionFromQValues(self,current_board) -> tuple[tuple[int, int], tuple[int, int]]:
        q_list=[self.getQValue(current_board,action) for action in self.game.getLegalActionsBySide(self.direction)]
        max_q=max(q_list)
        max_index=[]
        for i in range(len(q_list)):
            if q_list[i]==max_q:
                max_index.append(i)
        index=random.choice(max_index)
        # I recommend you saving `self.game.getLegalActionsBySide(self.direction)`, the method's result is not guaranteed to be stable
        # You may also use `enumerate`:
        """
                >>> a = [3, 6, 9, 11, 2]
                >>> for index, value in enumerate(a):
                ...     print(f"Index: {index}, Value: {value}")
        
                Index: 0, Value: 3
                Index: 1, Value: 6
                Index: 2, Value: 9
                Index: 3, Value: 11
                Index: 4, Value: 2
        """
        # Remember to remove this when you commit
        return self.game.getLegalActionsBySide(self.direction)[index]
        

    def update(self, current_board, action: tuple[tuple[int, int], tuple[int, int]], next_board, next_all_actions: list[tuple[tuple[int, int], tuple[int, int]]], reward: float):
        # get the old estimate
        old_estimate=self.getQValue(current_board,action)
        # compute max Q
        q_list=[self.getQValue(current_board,action) for action in next_all_actions]
        best_action=next_all_actions[q_list.index(max(q_list))]
        max_q=self.getQValue(next_board,best_action)
        sample=reward+self.discount*(max_q)
        # update the q_value
        self.q_value[(current_board,action)]=(1-self.alpha)*old_estimate+self.alpha*sample


    def getReward(self,action: tuple[tuple[int, int], tuple[int, int]]) ->float:
        """
            If the action has eaten one piece, return the corresponding reward;
            Else 0
        """
        eatenPieceType=self.game.board[action[1][0]][action[1][1]]
        if eatenPieceType==Piece.NoneType:
            return 0
        elif eatenPieceType==Piece.BSoldier:
            return 1
        elif eatenPieceType ==Piece.BAdvisor:
            return 2
        elif eatenPieceType ==Piece.BElephant:
            return 2
        elif eatenPieceType ==Piece.BHorse:
            return 4
        elif eatenPieceType ==Piece.BCannon:
            return 4.5
        elif eatenPieceType ==Piece.BChariot:
            return 9
        elif eatenPieceType ==Piece.BGeneral:
            return 100

    def get_next_board_and_action(self, action: tuple[tuple[int, int], tuple[int, int]]):
        # get next board
        src, dst=action[0],action[1]
        new_board=deepcopy(self.game.board)
        new_board[dst[0]][dst[1]] = new_board[src[0]][src[1]]
        new_board[src[0]][src[1]] = Piece.NoneType

        # get next pieces
        all_pieces=new_board.getSide()

        # get all actions
        actions=[]
        for piece in all_pieces:
            possible_position=new_board.getRange(piece)
            for position in possible_position:
                actions.append((piece,position))

        # convert new_board to tuple for hashing
        new_board=tuple(tuple(x) for x in new_board)
        return new_board,actions
        


    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
        # get action
        action=self.computeActionFromQValues(self.game)
        # get reward
        reward=self.getReward(action)
        # update
        next_board,next_all_actions=self.get_next_board_and_action(action)
        self.update(self.game,action,next_board,next_all_actions,reward)
        return action

