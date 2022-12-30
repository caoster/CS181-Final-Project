from queue import Queue

from ExampleAgent import ExampleAgent
from HumanPlayer.mouseAgent import MouseAgent
from agent import Agent
from gameModel import GameModel
from gameView import GameView, NoGraphic
from utils import Player, Counter, Piece
from ReinforcementLearning.qlearningAgent import QLearningAgent
from Adversarial.MinimaxAgent import MinimaxAgent
from MCTS.MCTSAgent import MCTSAgent
import json


def readConfig():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--res2", action="store_true", help="Use (more than) 2 times resolution, this option is OFF by default.")
    parser.add_argument("-r4", "--res4", action="store_true", help="Use (more than) 4 times resolution, this option is OFF by default.")
    parser.add_argument("-t", "--time", action="store", type=float, default=1.0,
                        help="The time interval in seconds between calling step functions, default interval is 1.0 second.")
    parser.add_argument("-R", "--Red", action="store", type=str, default="MouseAgent", help="The player of red side, default using MouseAgent.")
    parser.add_argument("-B", "--Black", action="store", type=str, default="ExampleAgent", help="The player of black side, default using ExampleAgent.")
    parser.add_argument("-n", "--no-graphic", action="store_true", help="Turn off graphic, this option will disable -r and -r4.")
    parser.add_argument("-m", "--num-of-matches", action="store", type=int, default=1, help="If the value is greater than 1, -n is enabled automatically.")
    parser.add_argument("-p", "--parallel", action="store", type=int, default=1, help="The maximum number of processes allowed.")
    args = parser.parse_args()
    return args


def initAgent(side: Player, choice: str, relate_view: GameView, q_value=None) -> Agent:
    if choice == "MouseAgent":
        agent = MouseAgent(side)
        tunnel = Queue(1)
        agent.setTunnelIn(tunnel)
        relate_view.enableMouse(side, tunnel)
    elif choice == "ExampleAgent":
        agent = ExampleAgent(side)
    elif choice == "QlearningAgent":
        agent = QLearningAgent(direction=side, q_value=q_value)
    elif choice == "MinimaxAgent":
        agent = MinimaxAgent(side)
    elif choice == "MCTSAgent":
        agent = MCTSAgent(side)
    else:
        assert False, "No such agent!"
    return agent


def remap_keys(q_value: Counter):
    return_list = []
    for k, v in q_value.items():
        new_k = []
        for i in range(9):
            new_k.append([])
            for j in range(10):
                if k[0][i][j]==Piece.NoneType:
                    new_k[i].append(0)
                elif k[0][i][j]==Piece.BGeneral:
                    new_k[i].append(1)
                elif k[0][i][j]==Piece.BAdvisor:
                    new_k[i].append(2)
                elif k[0][i][j]==Piece.BElephant:
                    new_k[i].append(3)
                elif k[0][i][j]==Piece.BHorse:
                    new_k[i].append(4)
                elif k[0][i][j]==Piece.BChariot:
                    new_k[i].append(5)
                elif k[0][i][j]==Piece.BCannon:
                    new_k[i].append(6)
                elif k[0][i][j]==Piece.BSoldier:
                    new_k[i].append(7)
                elif k[0][i][j]==Piece.RGeneral:
                    new_k[i].append(8)
                elif k[0][i][j]==Piece.RAdvisor:
                    new_k[i].append(9)
                elif k[0][i][j]==Piece.RElephant:
                    new_k[i].append(10)
                elif k[0][i][j]==Piece.RHorse:
                    new_k[i].append(11)
                elif k[0][i][j]==Piece.RChariot:
                    new_k[i].append(12)
                elif k[0][i][j]==Piece.RCannon:
                    new_k[i].append(13)
                elif k[0][i][j]==Piece.RSoldier:
                    new_k[i].append(14)
        return_list.append({'key': (new_k, k[1]), 'value': v})

    return return_list


if __name__ == "__main__":
    config = readConfig()
    print(config)
    q_value = Counter()
    # file = open('checkpoint.txt', 'r')
    # next(file)
    # js = file.read()
    # list = json.loads(js)
    # q_value = Counter()
    # for dict in list:
    #     board = dict['key'][0]
    #     action = dict['key'][1]
    #     for i in range(9):
    #         for j in range(10):
    #             board[i][j] = json.loads(board[i][j])
    #             if board[i][j]['_name_'] == 'NoneType':
    #                 board[i][j] = Piece.NoneType
    #             elif board[i][j]['_name_'] == 'BGeneral':
    #                 board[i][j] = Piece.BGeneral
    #             elif board[i][j]['_name_'] == 'BAdvisor':
    #                 board[i][j] = Piece.BAdvisor
    #             elif board[i][j]['_name_'] == 'BElephant':
    #                 board[i][j] = Piece.BElephant
    #             elif board[i][j]['_name_'] == 'BHorse':
    #                 board[i][j] = Piece.BHorse
    #             elif board[i][j]['_name_'] == 'BChariot':
    #                 board[i][j] = Piece.BChariot
    #             elif board[i][j]['_name_'] == 'BCannon':
    #                 board[i][j] = Piece.BCannon
    #             elif board[i][j]['_name_'] == 'BSoldier':
    #                 board[i][j] = Piece.BSoldier
    #             elif board[i][j]['_name_'] == 'RGeneral':
    #                 board[i][j] = Piece.RGeneral
    #             elif board[i][j]['_name_'] == 'RAdvisor':
    #                 board[i][j] = Piece.RAdvisor
    #             elif board[i][j]['_name_'] == 'RElephant':
    #                 board[i][j] = Piece.RElephant
    #             elif board[i][j]['_name_'] == 'RHorse':
    #                 board[i][j] = Piece.RHorse
    #             elif board[i][j]['_name_'] == 'RChariot':
    #                 board[i][j] = Piece.RChariot
    #             elif board[i][j]['_name_'] == 'RCannon':
    #                 board[i][j] = Piece.RCannon
    #             elif board[i][j]['_name_'] == 'RSoldier':
    #                 board[i][j] = Piece.RSoldier
    #     value = dict['value']
    #     board = tuple(tuple(x) for x in board)
    #     action = tuple(tuple(x) for x in action)
    #     q_value[(board, action)] = value

    for i in range(10000000):
        view = NoGraphic()
        # view = GameView(2)
        red_agent = initAgent(Player.Red, config.Red, view, q_value)
        black_agent = initAgent(Player.Black, config.Black, view)
        model = GameModel(view, red_agent, black_agent, config.time)
        model.startApp()
        q_value = red_agent.getQValueBoard()
        js = json.dumps(remap_keys(q_value))
        file = open('checkpoints.txt', 'w')
        file.write("Training episode: {}\n".format(i + 1))
        file.write(js)
        print("Training episode: {}".format(i + 1))
        file.close()