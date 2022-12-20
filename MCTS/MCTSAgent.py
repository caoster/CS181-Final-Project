from __future__ import annotations

import math
import random

from agent import Agent
from gameModel import GameState
from utils import Player


class MCTSGameState(GameState):
    def __init__(self):
        super().__init__()

    def calRewardFromState(self) -> float:
        raise NotImplemented


class MCTSnode:
    def __init__(self):
        self.parent = None
        self.state = None
        self.all_valid_actions = None
        self.children: dict[GameState: tuple[MCTSnode, tuple[tuple[int, int], tuple[int, int]]]] = {}
        self.visit_time: int = 0
        self.quality_value: float = 0.0

    def setState(self, state: MCTSGameState):
        self.state = state

    def setParent(self, parent: MCTSnode):
        self.parent = parent

    def setVisitTime(self, visit_time: int):
        self.visit_time = visit_time

    def setQualityValue(self, quality_value: float):
        self.quality_value = quality_value

    def is_all_expand(self) -> bool:
        if self.all_valid_actions is None:
            self.find_all_valid_actions()
        return len(self.children) == len(self.all_valid_actions)

    def find_all_valid_actions(self):
        # if self.all_valid_actions is not None:
        #     return
        # self.all_valid_actions: Optional[(tuple, tuple)] = []
        # self.state: GameState
        # all_pieces = self.state.getSide(self.state.myself)
        # for piece in all_pieces:
        #     possible_pos = self.state.getRange(piece)
        #     for pos in possible_pos:
        #         self.all_valid_actions.append(piece, pos)
        return self.state.getLegalActionsBySide(self.state.myself)

    def expand(self) -> MCTSnode:
        next_state, action = self.randomChooseNextState()
        next_node = MCTSnode()
        next_node.setState(next_state)
        self.children[next_state] = (next_node, action)
        next_node.parent = self
        return next_node

    def randomChooseNextState(self) -> tuple[MCTSGameState, tuple[tuple[int, int], tuple[int, int]]]:
        choice = random.choice(self.all_valid_actions)
        next_state = self.state.getNextState(choice)
        while next_state in self.children.keys():
            choice = random.choice(self.all_valid_actions)
            next_state = self.state.getNextState(choice)
        return next_state, choice

    def bestChild(self, is_exploration: bool) -> tuple[MCTSnode, tuple[tuple[int, int], tuple[int, int]]]:
        best_score = -float('inf')
        best_child = None
        best_action = None
        for child, action in self.children.values():
            child: MCTSnode
            if is_exploration:
                c = 1 / math.sqrt(2.0)
            else:
                c = 0.0

            UCB = self.calUCB(c, child)
            if UCB > best_score:
                best_child = child
                best_score = UCB
                best_action = action

        return best_child, best_action

    def calUCB(self, c: float, child: MCTSnode) -> float:
        # UCB = quality_value / visit_time + c * sqrt(2 * ln(parent_visit_time) / visit_time)
        return child.quality_value / child.visit_time + c * math.sqrt(2 * math.log(self.visit_time) / child.visit_time)


class MCTSAgent(Agent):

    def __init__(self, direction: Player, node: MCTSnode, computation_budget: int):
        super().__init__(direction)
        self.root = node
        self.computation_budget = computation_budget

    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
        for i in range(self.computation_budget):
            expand_node = self.treePolicy(self.root)
            reward = self.defaultPolicy(expand_node)
            self.backup(expand_node, reward)
        self.root, action = self.root.bestChild(False)
        return action

    @staticmethod
    def treePolicy(node: MCTSnode) -> MCTSnode:
        if node.state.isMatchOver() == Player.NoneType:
            if node.is_all_expand():
                node = node.bestChild(True)
            else:
                expand_node = node.expand()
                return expand_node
        return node

    @staticmethod
    def defaultPolicy(node: MCTSnode) -> float:
        while node.state.isMatchOver() == Player.NoneType:
            node = node.expand()
        return node.state.calRewardFromState()

    @staticmethod
    def backup(node: MCTSnode, reward: float):
        leaf_side = node.state.myself
        while node is not None:
            node.visit_time += 1
            if node.state.myself == leaf_side:
                node.quality_value += reward
            else:
                node.quality_value -= reward
            node = node.parent
