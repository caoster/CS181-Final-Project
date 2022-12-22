from __future__ import annotations

import math
import random

import numpy as np

from agent import Agent
from gameModel import GameState
from utils import Player


class MCTSnode:
    def __init__(self):
        self.parent = None
        self.state = None
        self.all_valid_actions = None
        self.children: dict[GameState: tuple[MCTSnode, tuple[tuple[int, int], tuple[int, int]]]] = {}
        self.visit_time: int = 0
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
        if self.all_valid_actions is None:
            self.find_all_valid_actions()
        return len(self.children) == len(self.all_valid_actions)

    def find_all_valid_actions(self):
        self.all_valid_actions = self.state.getLegalActionsBySide(self.state.myself)

    def expand(self) -> MCTSnode:
        next_state, action = self.randomChooseNextState()
        next_node = MCTSnode()
        next_node.setState(next_state)
        self.children[next_state] = (next_node, action)
        next_node.parent = self
        return next_node

    def randomChooseNextState(self) -> tuple[GameState, tuple[tuple[int, int], tuple[int, int]]]:
        if self.all_valid_actions is None:
            self.find_all_valid_actions()
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
        if is_exploration:
            c = 1 / math.sqrt(2.0)
        else:
            c = 0.0
        UCB_list = np.array([self.calUCB(c, child) for child, _ in self.children.values()])
        best_score = np.amax(UCB_list)
        best_idx = np.argwhere(np.isclose(UCB_list, best_score, 1.e-3, 1.e-5)).squeeze()
        if best_idx.size != 0:
            best_choice = np.random.choice(best_idx)
        else:
            best_choice = np.argmax(UCB_list)
        best_child, best_action = list(self.children.values())[best_choice]

        return best_child, best_action

    def calRewardFromState(self, direction: Player) -> float:
        winner = self.state.getWinner()
        if winner == direction:
            return 10
        elif winner == Player.reverse(direction):
            return -10

    def calUCB(self, c: float, child: MCTSnode) -> float:
        # UCB = quality_value / visit_time + c * sqrt(2 * ln(parent_visit_time) / visit_time)
        return child.quality_value / (child.visit_time + 1e-5) + c * math.sqrt(2 * math.log(self.visit_time + 1) / (child.visit_time + 1e-5))


class MCTSAgent(Agent):

    def __init__(self, direction: Player, computation_budget: int = 1000):
        super().__init__(direction)
        self.root = None
        self.computation_budget = computation_budget

    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
        self.root = MCTSnode()
        self.root.setState(self.game.getGameState())
        self.root.state.myself = self.direction
        self.root.find_all_valid_actions()
        print(len(self.root.all_valid_actions))
        for i in range(self.computation_budget):
            expand_node = self.treePolicy(self.root)
            reward = self.defaultPolicy(expand_node)
            self.backup(expand_node, reward)
        print(*[ch.visit_time for ch, _ in self.root.children.values()])

        self.root, action = self.root.bestChild(False)
        return action

    @staticmethod
    def treePolicy(node: MCTSnode) -> MCTSnode:
        if not node.state.isMatchOver():
            if node.is_all_expand():
                node, _ = node.bestChild(True)
            else:
                expand_node = node.expand()
                return expand_node
        return node

    def defaultPolicy(self, node: MCTSnode) -> float:
        while not node.state.isMatchOver():
            node = node.expand()
        return node.calRewardFromState(self.direction)

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
