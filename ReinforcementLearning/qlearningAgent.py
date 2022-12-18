from typing import Optional
from agent import Agent
from utils import Piece, Player, Counter
from gameModel import GameModel
import random



class QLearningAgent(Agent):
    def __init__(self, direction: Player, numTraining=100, alpha=0.2, gamma=0.8 ,q_value=None):
        """
        alpha    - learning rate
        gamma    - discount factor
        numTraining - number of training episodes
        """
        self.game: Optional[GameModel] = None
        self.direction: Player = direction

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
    
    def getLegalActions(self) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        all_pieces = self.game.getSide(self.direction) 
        actions=[]
        for piece in all_pieces:
            possible_position=self.game.getRange(piece)
            for position in possible_position:
                actions.append((piece,position))
        return actions


    def getQValue(self, current_board, action: tuple[tuple[int, int], tuple[int, int]]) -> float:

        return self.q_value[(current_board,action)]


    def computeValueFromQValues(self, current_board) -> float:
        if self.getLegalActions(current_board)==None:
            return None
        best_action=self.computeActionFromQValues(current_board)
        return self.getQValue(current_board,best_action)
        

    def computeActionFromQValues(self,current_board) -> tuple[tuple[int, int], tuple[int, int]]:
        q_list=[self.getQValue(current_board,action) for action in self.getLegalActions()]
        max_q=max(q_list)
        max_index=[]
        for i in range(len(q_list)):
            if q_list[i]==max_q:
                max_index.append(i)
        index=random.choice(max_index)
        return self.getLegalActions()[index]
        

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
    
    def findPiece(self, new_board, condition: callable) -> list[tuple[int, int]]:
        pieces=[]
        for i, x in enumerate(new_board):
            pieces += [(i, j) for j, y in enumerate(x) if condition(y)]
        return pieces

    def get_next_board_and_action(self, action: tuple[tuple[int, int], tuple[int, int]]):
        # get next board
        src, dst=action[0],action[1]
        new_board=[]
        for i in range(9):
            new_board.append([])
            for j in range(10):
                new_board[i].append(self.game.board[i][j])
        new_board[dst[0]][dst[1]] = new_board[src[0]][src[1]]
        new_board[src[0]][src[1]] = Piece.NoneType

        # get next pieces
        all_pieces=self.findPiece(new_board,lambda a: Piece.getSide(a) == self.direction)

        # get all actions
        actions=[]
        for piece in all_pieces:
            possible_position=self.getAllAction(new_board,piece)
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


    def getAllAction(self, new_board, position: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = position
        pieceType = new_board[x][y]
        result: list[tuple[int, int]] = []
        if pieceType == Piece.NoneType:
            return result

        def checkEmpty(loc_x, loc_y):
            return new_board[loc_x][loc_y] == Piece.NoneType

        def inRangeAndEmpty(loc_x, loc_y):
            if inRange(loc_x, loc_y):
                return new_board[loc_x][loc_y] == Piece.NoneType
            return False

        def inRange(loc_x, loc_y):
            return 0 <= loc_x < 9 and 0 <= loc_y < 10

        def checkForBlack(loc_x, loc_y):
            if Piece.getSide(new_board[loc_x][loc_y]) != Player.Black:
                result.append((loc_x, loc_y))

        def checkForRed(loc_x, loc_y):
            if Piece.getSide(new_board[loc_x][loc_y]) != Player.Red:
                result.append((loc_x, loc_y))

        def safeCheckForBlack(loc_x, loc_y):
            if inRange(loc_x, loc_y):
                checkForBlack(loc_x, loc_y)

        def safeCheckForRed(loc_x, loc_y):
            if inRange(loc_x, loc_y):
                checkForRed(loc_x, loc_y)

        if pieceType == Piece.BGeneral:  # 1
            if position == (3, 0):
                checkForBlack(3, 1)
                checkForBlack(4, 0)
            elif position == (3, 1):
                checkForBlack(3, 0)
                checkForBlack(4, 1)
                checkForBlack(3, 2)
            elif position == (3, 2):
                checkForBlack(3, 1)
                checkForBlack(4, 2)
            elif position == (4, 0):
                checkForBlack(3, 0)
                checkForBlack(4, 1)
                checkForBlack(5, 0)
            elif position == (4, 1):
                checkForBlack(3, 1)
                checkForBlack(4, 0)
                checkForBlack(4, 2)
                checkForBlack(5, 1)
            elif position == (4, 2):
                checkForBlack(4, 1)
                checkForBlack(3, 2)
                checkForBlack(5, 2)
            elif position == (5, 0):
                checkForBlack(4, 0)
                checkForBlack(5, 1)
            elif position == (5, 1):
                checkForBlack(5, 0)
                checkForBlack(4, 1)
                checkForBlack(5, 2)
            elif position == (5, 2):
                checkForBlack(5, 1)
                checkForBlack(4, 2)

        elif pieceType == Piece.BAdvisor:  # 2
            if position == (3, 0):
                checkForBlack(4, 1)
            elif position == (5, 0):
                checkForBlack(4, 1)
            elif position == (3, 2):
                checkForBlack(4, 1)
            elif position == (5, 2):
                checkForBlack(4, 1)
            elif position == (4, 1):
                checkForBlack(3, 0)
                checkForBlack(5, 0)
                checkForBlack(3, 2)
                checkForBlack(5, 2)

        elif pieceType == Piece.BElephant:  # 3
            if inRangeAndEmpty(x - 1, y - 1) and 0 <= y - 2 <= 4:
                safeCheckForBlack(x - 2, y - 2)
            if inRangeAndEmpty(x + 1, y - 1) and 0 <= y - 2 <= 4:
                safeCheckForBlack(x + 2, y - 2)
            if inRangeAndEmpty(x - 1, y + 1) and 0 <= y + 2 <= 4:
                safeCheckForBlack(x - 2, y + 2)
            if inRangeAndEmpty(x + 1, y + 1) and 0 <= y + 2 <= 4:
                safeCheckForBlack(x + 2, y + 2)

        elif pieceType == Piece.BHorse:  # 4
            if inRangeAndEmpty(x + 1, y):
                safeCheckForBlack(x + 2, y - 1)
                safeCheckForBlack(x + 2, y + 1)
            if inRangeAndEmpty(x, y + 1):
                safeCheckForBlack(x + 1, y + 2)
                safeCheckForBlack(x - 1, y + 2)
            if inRangeAndEmpty(x - 1, y):
                safeCheckForBlack(x - 2, y + 1)
                safeCheckForBlack(x - 2, y - 1)
            if inRangeAndEmpty(x, y - 1):
                safeCheckForBlack(x - 1, y - 2)
                safeCheckForBlack(x + 1, y - 2)

        elif pieceType == Piece.BChariot:  # 5
            # Direction: right
            for i in range(1, 10):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                checkForBlack(x + i, y)
                break
            # Direction: left
            for i in range(1, 10):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                checkForBlack(x - i, y)
                break
            # Direction: up
            for i in range(1, 10):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                checkForBlack(x, y - i)
                break
            # Direction: down
            for i in range(1, 10):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                checkForBlack(x, y + i)
                break

        elif pieceType == Piece.BCannon:  # 6
            # Direction: right
            for i in range(1, 10):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x + j, y):
                        break
                    if not checkEmpty(x + j, y):
                        if Piece.getSide(new_board[x + j][y]) == Player.Red:
                            result.append((x + j, y))
                        break
                break
            # Direction: left
            for i in range(1, 10):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x - j, y):
                        break
                    if not checkEmpty(x - j, y):
                        if Piece.getSide(new_board[x - j][y]) == Player.Red:
                            result.append((x - j, y))
                        break
                break
            # Direction: up
            for i in range(1, 10):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x, y - j):
                        break
                    if not checkEmpty(x, y - j):
                        if Piece.getSide(new_board[x][y - j]) == Player.Red:
                            result.append((x, y - j))
                        break
                break
            # Direction: down
            for i in range(1, 10):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x, y + j):
                        break
                    if not checkEmpty(x, y + j):
                        if Piece.getSide(new_board[x][y + j]) == Player.Red:
                            result.append((x, y + j))
                        break
                break

        elif pieceType == Piece.BSoldier:  # 7
            if y <= 4:
                checkForBlack(x, y + 1)
            else:
                safeCheckForBlack(x, y + 1)
                safeCheckForBlack(x - 1, y)
                safeCheckForBlack(x + 1, y)

        elif pieceType == Piece.RGeneral:  # 8
            if position == (3, 9):
                checkForRed(3, 8)
                checkForRed(4, 9)
            elif position == (4, 9):
                checkForRed(3, 9)
                checkForRed(5, 9)
                checkForRed(4, 8)
            elif position == (5, 9):
                checkForRed(4, 9)
                checkForRed(5, 8)
            elif position == (3, 8):
                checkForRed(3, 7)
                checkForRed(4, 8)
                checkForRed(3, 9)
            elif position == (4, 8):
                checkForRed(3, 8)
                checkForRed(4, 9)
                checkForRed(5, 8)
                checkForRed(4, 7)
            elif position == (5, 8):
                checkForRed(4, 8)
                checkForRed(5, 7)
                checkForRed(5, 9)
            elif position == (3, 7):
                checkForRed(3, 8)
                checkForRed(4, 7)
            elif position == (4, 7):
                checkForRed(3, 7)
                checkForRed(4, 8)
                checkForRed(5, 7)
            elif position == (5, 7):
                checkForRed(4, 7)
                checkForRed(5, 8)

        elif pieceType == Piece.RAdvisor:  # 9
            if position == (3, 9):
                checkForRed(4, 8)
            elif position == (3, 7):
                checkForRed(4, 8)
            elif position == (5, 7):
                checkForRed(4, 8)
            elif position == (5, 9):
                checkForRed(4, 8)
            elif position == (4, 8):
                checkForRed(3, 7)
                checkForRed(3, 9)
                checkForRed(5, 7)
                checkForRed(5, 9)

        elif pieceType == Piece.RElephant:  # 10
            if inRangeAndEmpty(x - 1, y - 1) and 5 <= y - 2 <= 9:
                safeCheckForRed(x - 2, y - 2)
            if inRangeAndEmpty(x + 1, y - 1) and 5 <= y - 2 <= 9:
                safeCheckForRed(x + 2, y - 2)
            if inRangeAndEmpty(x - 1, y + 1) and 5 <= y + 2 <= 9:
                safeCheckForRed(x - 2, y + 2)
            if inRangeAndEmpty(x + 1, y + 1) and 5 <= y + 2 <= 9:
                safeCheckForRed(x + 2, y + 2)

        elif pieceType == Piece.RHorse:  # 11
            if inRangeAndEmpty(x + 1, y):
                safeCheckForRed(x + 2, y - 1)
                safeCheckForRed(x + 2, y + 1)
            if inRangeAndEmpty(x, y + 1):
                safeCheckForRed(x + 1, y + 2)
                safeCheckForRed(x - 1, y + 2)
            if inRangeAndEmpty(x - 1, y):
                safeCheckForRed(x - 2, y + 1)
                safeCheckForRed(x - 2, y - 1)
            if inRangeAndEmpty(x, y - 1):
                safeCheckForRed(x - 1, y - 2)
                safeCheckForRed(x + 1, y - 2)

        elif pieceType == Piece.RChariot:  # 12
            # Direction: right
            for i in range(1, 10):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                checkForRed(x + i, y)
                break
            # Direction: left
            for i in range(1, 10):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                checkForRed(x - i, y)
                break
            # Direction: up
            for i in range(1, 10):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                checkForRed(x, y - i)
                break
            # Direction: down
            for i in range(1, 10):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                checkForRed(x, y + i)
                break

        elif pieceType == Piece.RCannon:  # 13
            # Direction: right
            for i in range(1, 10):
                if not inRange(x + i, y):
                    break
                if checkEmpty(x + i, y):
                    result.append((x + i, y))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x + j, y):
                        break
                    if not checkEmpty(x + j, y):
                        if Piece.getSide(new_board[x + j][y]) == Player.Black:
                            result.append((x + j, y))
                        break
                break
            # Direction: left
            for i in range(1, 10):
                if not inRange(x - i, y):
                    break
                if checkEmpty(x - i, y):
                    result.append((x - i, y))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x - j, y):
                        break
                    if not checkEmpty(x - j, y):
                        if Piece.getSide(new_board[x - j][y]) == Player.Black:
                            result.append((x - j, y))
                        break
                break
            # Direction: up
            for i in range(1, 10):
                if not inRange(x, y - i):
                    break
                if checkEmpty(x, y - i):
                    result.append((x, y - i))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x, y - j):
                        break
                    if not checkEmpty(x, y - j):
                        if Piece.getSide(new_board[x][y - j]) == Player.Black:
                            result.append((x, y - j))
                        break
                break
            # Direction: down
            for i in range(1, 10):
                if not inRange(x, y + i):
                    break
                if checkEmpty(x, y + i):
                    result.append((x, y + i))
                    continue
                for j in range(i + 1, 10):
                    if not inRange(x, y + j):
                        break
                    if not checkEmpty(x, y + j):
                        if Piece.getSide(new_board[x][y + j]) == Player.Black:
                            result.append((x, y + j))
                        break
                break

        elif pieceType == Piece.RSoldier:  # 14
            if y >= 5:
                checkForRed(x, y - 1)
            else:
                safeCheckForRed(x, y - 1)
                safeCheckForRed(x - 1, y)
                safeCheckForRed(x + 1, y)

        return result