from __future__ import annotations

import math
import random

import numpy as np

from agent import Agent
from gameModel import GameState
from utils import Player


class MCTSnode:
    def __init__(self):
        self.num_all_valid_actions = None
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
        return len(self.children) == self.num_all_valid_actions

    def find_all_valid_actions(self):
        self.all_valid_actions = self.state.getLegalActionsBySide(self.state.myself)
        self.num_all_valid_actions = len(self.all_valid_actions)

    def expand(self) -> MCTSnode:
        next_state, action = self.randomChooseNextState()
        next_node = MCTSnode()
        next_node.setState(next_state)
        next_node.find_all_valid_actions()
        self.children[next_state] = (next_node, action)
        next_node.parent = self
        return next_node

    def randomExpand(self) -> MCTSnode:
        action = random.choice(self.all_valid_actions)
        next_state = self.state.getNextState(action)
        if next_state not in self.children.keys():
            next_node = MCTSnode()
            next_node.setState(next_state)
            next_node.find_all_valid_actions()
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

        return best_child, best_action

    def calRewardFromState(self, direction: Player) -> float:
        winner = self.state.getWinner()
        if winner == direction:
            return 0
        elif winner == Player.reverse(direction):
            return 0

    def calUCB(self, c: float, child: MCTSnode) -> float:
        # UCB = quality_value / visit_time + c * sqrt(2 * ln(parent_visit_time) / visit_time)
        if child.visit_time == 0:
            return 0.0
        UCB = child.quality_value / child.visit_time + c * math.sqrt(2 * math.log(self.visit_time) / child.visit_time)
        return UCB


class MCTSAgent(Agent):

    def __init__(self, direction: Player, computation_budget: int = 400):
        super().__init__(direction)
        self.root = MCTSnode()
        self.computation_budget = computation_budget

    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
        new_state = self.game.getGameState()
        if new_state in self.root.children.keys():
            self.root, _ = self.root.children[new_state]
            self.root.parent = None
        else:
            self.root = MCTSnode()
            self.root.setState(new_state)
            self.root.state.myself = self.direction
        self.root.find_all_valid_actions()
        # print(len(self.root.all_valid_actions))
        for i in range(self.computation_budget):
            expand_node = self.treePolicy(self.root)  # expand one node
            expand_node, reward = self.defaultPolicy(expand_node)
            self.backup(expand_node, reward, self.direction)
        print(*[child.visit_time for child, _ in self.root.children.values()])

        self.root, action = self.root.bestChild(False)
        print(action)
        return action

    @staticmethod
    def treePolicy(node: MCTSnode) -> MCTSnode:
        if not node.state.isMatchOver():
            if node.is_all_expand():
                node, _ = node.bestChild(True)
            else:
                return node.expand()
        return node

    def defaultPolicy(self, node: MCTSnode) -> float:
        round_limit = 600
        r = 0
        while not node.state.isMatchOver():
            # node = self.treePolicy(node)
            node = node.randomExpand()
            r += 1
            if r > round_limit:
                print("tie!")
                return node, 0
        return node, node.calRewardFromState(self.direction)

    @staticmethod
    def backup(node: MCTSnode, reward: float, direction: Player):
        # TODO: Verify direction/Player. Verify the Pieces got by indexing with actions.
        evaluate = [[0, 0, 0, 1, 1, 1, 1],
                    [0, 0, 0, 9.5, 14.5, 10, 7],
                    [0, 0, 0, 9.5, 14.5, 10, 7],
                    [50, 5.5, 5.5, 7.5, 12.5, 8, 5],
                    [50, 0.5, 0.5, 2.5, 7.5, 3, 0],
                    [50, 5, 5, 7, 12, 7.5, 4.5],
                    [50, 8, 8, 10, 15, 10.5, 7.5]]
        whole = np.zeros((15, 15))
        whole[1:8, 8:15] = np.array(evaluate)
        whole[8:15, 1:8] = np.array(evaluate)
        while node.parent is not None:
            node.visit_time += 1
            parent = node.parent
            _, action = parent.children[node.state]
            consumer = int(parent.state.board[action[0][0]][action[0][1]])
            consumee = int(parent.state.board[action[1][0]][action[1][1]])
            if node.state.myself == direction:
                reward = 0.9 * reward - whole[consumer][consumee]
                node.quality_value += reward
            else:
                reward = 0.9 * reward + whole[consumer][consumee]
                node.quality_value -= reward
            node = node.parent
        node.visit_time += 1
