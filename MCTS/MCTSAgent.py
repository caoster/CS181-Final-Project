from __future__ import annotations

import math
import random

import numpy as np

from agent import Agent
from gameModel import GameState
from utils import Player, Piece
from data import EvaluationMatrix


class MCTSnode:
    def __init__(self):
        self.num_all_valid_actions = None
        self.parent = None
        self.state = None
        self.all_valid_actions = None
        self.children: dict[GameState: tuple[MCTSnode, tuple[tuple[int, int], tuple[int, int]]]] = {}
        self.visit_time: int = 0
        self.no_consume: int = 0
        self.quality_value: float = 0.0

    def setState(self, state: GameState):
        self.state = state

    def setParent(self, parent: MCTSnode):
        self.parent = parent

    def setVisitTime(self, visit_time: int):
        self.visit_time = visit_time

    def setQualityValue(self, quality_value: float):
        self.quality_value = quality_value

    def is_all_expand(self) -> bool:
        return len(self.children) == self.num_all_valid_actions

    def find_all_valid_actions(self):
        self.all_valid_actions = self.state.getLegalActionsBySide(self.state.myself)
        if self.state.myself == Player.Red:
            my_general = Piece.RGeneral
            other_general = Piece.BGeneral
        elif self.state.myself == Player.Black:
            my_general = Piece.BGeneral
            other_general = Piece.RGeneral
        # checkmate opponent
        attack = self.state.getThreatBySide(Player.reverse(self.state.myself))
        other_piece_pos = self.state.findPiece(other_general)
        if other_piece_pos != [] and attack[other_piece_pos[0]] != []:
            actions = []
            for my_piece_pos in attack[other_piece_pos[0]]:
                actions.append((my_piece_pos, other_piece_pos[0]))
            self.all_valid_actions = actions
            self.num_all_valid_actions = len(self.all_valid_actions)
            return
        # avoid direct checkmate
        threats = self.state.getThreatBySide(self.state.myself)
        my_piece_pos = self.state.findPiece(my_general)
        if my_piece_pos != [] and threats[my_piece_pos[0]] != []:
            actions = []
            for action in self.all_valid_actions:
                state = self.state.getNextState(action=action)
                new_threats = state.getThreatBySide(self.state.myself)
                my_new_piece_pos = state.findPiece(my_general)
                if my_new_piece_pos != [] and new_threats[my_new_piece_pos[0]] == []:
                    actions.append(action)
            if actions != []:
                self.all_valid_actions = actions
                self.num_all_valid_actions = len(self.all_valid_actions)
                return
        # avoid action lead to checkmate
        for action in self.all_valid_actions:
            state = self.state.getNextState(action=action)
            new_threats = state.getThreatBySide(self.state.myself)
            my_new_piece_pos = state.findPiece(my_general)
            if my_new_piece_pos != [] and new_threats[my_new_piece_pos[0]] != []:
                self.all_valid_actions.remove(action)
        self.num_all_valid_actions = len(self.all_valid_actions)

    def initQvalue(self, matrix: EvaluationMatrix) -> None:
        if Player.reverse(self.state.myself) == Player.Red:
            my_counter = {Piece.RGeneral: 1, Piece.RAdvisor: 2, Piece.RElephant: 2, Piece.RHorse: 2, Piece.RChariot: 2, Piece.RCannon: 2, Piece.RSoldier: 5}
            enemy_counter = {Piece.BGeneral: 1, Piece.BAdvisor: 2, Piece.BElephant: 2, Piece.BHorse: 2, Piece.BChariot: 2, Piece.BCannon: 2, Piece.BSoldier: 5}
        else:
            my_counter = {Piece.BGeneral: 1, Piece.BAdvisor: 2, Piece.BElephant: 2, Piece.BHorse: 2, Piece.BChariot: 2, Piece.BCannon: 2, Piece.BSoldier: 5}
            enemy_counter = {Piece.RGeneral: 1, Piece.RAdvisor: 2, Piece.RElephant: 2, Piece.RHorse: 2, Piece.RChariot: 2, Piece.RCannon: 2, Piece.RSoldier: 5}
        myPiece = self.state.getSide(Player.reverse(self.state.myself))
        enemyPiece = self.state.getSide(self.state.myself)
        myThreat = self.state.getThreatBySide(Player.reverse(self.state.myself))
        score = 0
        for piece in myPiece:
            pieceType = self.state[piece[0]][piece[1]]
            my_counter[pieceType] -= 1
            score += matrix.pieceValue[pieceType] * matrix.pieceScore[pieceType][piece[0]][piece[1]]
            attack_pos = self.state.getRange(piece)
            for threat in myThreat[piece]:
                score -= matrix.pieceValue[pieceType]
            for position in attack_pos:
                x, y = position
                pieceType = self.state[x][y]
                score += matrix.pieceValue[pieceType]
        for piece in enemyPiece:
            pieceType = self.state[piece[0]][piece[1]]
            enemy_counter[pieceType] -= 1
            score -= matrix.pieceValue[pieceType] * matrix.pieceScore[pieceType][piece[0]][piece[1]]
        for piece in my_counter.keys():
            score -= my_counter[piece] * matrix.pieceValue[piece]
        for piece in enemy_counter.keys():
            score += enemy_counter[piece] * matrix.pieceValue[piece]
        self.quality_value = score

    def expand(self) -> MCTSnode:
        next_state, action = self.randomChooseNextState()
        next_node = MCTSnode()
        next_node.setState(next_state)
        next_node.find_all_valid_actions()
        self.children[next_state] = (next_node, action)
        next_node.parent = self
        return next_node

    def randomExpand(self, matrix: EvaluationMatrix) -> MCTSnode:
        action = random.choice(self.all_valid_actions)
        next_state = self.state.getNextState(action)
        if next_state not in self.children.keys():
            next_node = MCTSnode()
            next_node.setState(next_state)
            next_node.find_all_valid_actions()
            next_node.initQvalue(matrix)
            self.children[next_state] = (next_node, action)
            next_node.parent = self
        else:
            next_node = self.children[next_state][0]
        return next_node

    def randomChooseNextState(self) -> tuple[GameState, tuple[tuple[int, int], tuple[int, int]]]:
        if len(self.all_valid_actions) == 0:
            print("Error: all_valid_actions has already been an empty list but still get access to randomChooseNextState function!")
        # elif len(self.all_valid_actions) == 1:
        #     choice = self.all_valid_actions[0]
        else:
            choice = random.choice(self.all_valid_actions)
        self.all_valid_actions.remove(choice)
        next_state = self.state.getNextState(choice)
        return next_state, choice

    def bestChild(self, is_exploration: bool) -> tuple[MCTSnode, tuple[tuple[int, int], tuple[int, int]]]:
        if is_exploration:
            c = 1 / math.sqrt(2.0)
        else:
            c = 0.0
        UCB_list = np.array([self.calUCB(c, child) for child, _ in self.children.values()])
        best_score = np.amax(UCB_list)
        best_idx = np.argwhere(np.isclose(UCB_list, best_score)).squeeze()
        if best_idx.size > 1:
            best_choice = np.random.choice(best_idx)
        else:
            best_choice = np.argmax(UCB_list)
        best_child, best_action = list(self.children.values())[best_choice]
        if not is_exploration:
            # best_child: MCTSnode
            print(f"choose child node with visit_time = {best_child.visit_time}")
        return best_child, best_action

    def calRewardFromState(self, direction: Player) -> float:
        winner = self.state.getWinner()
        # if self.state.findPiece(Piece.RGeneral) is not [] and self.state.findPiece(Piece.BGeneral) is not []:
        if winner == direction:
            return 1
        elif winner == Player.reverse(direction):
            return -1
        return 0

    def calUCB(self, c: float, child: MCTSnode) -> float:
        # UCB = quality_value / visit_time + c * sqrt(2 * ln(parent_visit_time) / visit_time)
        if child.visit_time == 0:
            return 0.0
        UCB = child.quality_value / child.visit_time + c * math.sqrt(2 * math.log(self.visit_time) / child.visit_time)
        return UCB


class MCTSAgent(Agent):
    def __init__(self, direction: Player, computation_budget: int = 100):
        super().__init__(direction)
        self.root = MCTSnode()
        self.evaluate_matrix = EvaluationMatrix()
        self.computation_budget = computation_budget
        self.tie = 0
        for key in self.evaluate_matrix.pieceValue.keys():
            self.evaluate_matrix.pieceValue[key] /= 10000
        # self.evaluate_matrix.pieceValue["compensate"] = self.evaluate_matrix.pieceValue[Piece.RChariot]

    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
        print("MCTS starts thinking!")
        new_state = self.game.getGameState()
        if new_state in self.root.children.keys():
            self.root, _ = self.root.children[new_state]
            self.root.parent = None
        else:
            self.root = MCTSnode()
            self.root.setState(new_state)
            self.root.initQvalue(self.evaluate_matrix)
            self.root.state.myself = self.direction
        self.root.find_all_valid_actions()
        # print(len(self.root.all_valid_actions))
        self.tie = 0
        for i in range(self.computation_budget):
            expand_node = self.treePolicy(self.root)  # expand one node
            expand_node, reward = self.defaultPolicy(expand_node)
            self.backup(expand_node, reward)
        print(self.tie)
        for child, _ in self.root.children.values():
            print(f"{child.visit_time}: {child.quality_value / child.visit_time}")
        # print(*[f"{child.visit_time}: {child.quality_value}" for child, _ in self.root.children.values()])
        self.root, action = self.root.bestChild(False)
        print("MCTS stops thinking.")
        return action

    # @staticmethod
    def treePolicy(self, node: MCTSnode) -> MCTSnode:
        if not node.state.isMatchOver():
            if node.is_all_expand():
                node, _ = node.bestChild(True)
            else:
                node = node.expand()
                node.initQvalue(self.evaluate_matrix)
                return node
        return node

    def defaultPolicy(self, node: MCTSnode) -> tuple[MCTSnode, float]:
        round_limit = 200
        r = 0
        while not node.state.isMatchOver():
            # node = self.treePolicy(node)
            node = node.randomExpand(self.evaluate_matrix)
            r += 1
            if r > round_limit:
                self.tie += 1
                return node, 0
        node.state.swapDirection()
        reward = node.calRewardFromState(self.direction)
        node.state.swapDirection()
        return node, reward

    # @staticmethod
    def backup(self, node: MCTSnode, reward: float):
        while node.parent is not None:
            node.visit_time += 1
            parent = node.parent
            _, action = parent.children[node.state]
            consumer = parent.state[action[0][0]][action[0][1]]
            consumee = parent.state[action[1][0]][action[1][1]]
            if consumee == Piece.NoneType:
                consumer = Piece.NoneType
            if node.state.myself == self.direction:
                # reward = 0.9 * reward
                node.quality_value -= reward
            else:
                # reward = 0.9 * reward
                node.quality_value += reward
            node = node.parent
        node.visit_time += 1
