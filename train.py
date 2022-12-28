from queue import Queue

from ExampleAgent import ExampleAgent
from HumanPlayer.mouseAgent import MouseAgent
from agent import Agent
from gameModel import GameModel
from gameView import GameView, NoGraphic
from utils import Player, Counter
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
                #         k[0][i][j]=json.dumps(obj=k[0][i][j].__dict__,ensure_ascii=False, default=str)
                new_k[i].append(json.dumps(obj=k[0][i][j].__dict__, ensure_ascii=False, default=str))
        # k[0]=json.dumps(obj=k[0].__dict__,ensure_ascii=False)
        return_list.append({'key': (new_k, k[1]), 'value': v})

    return return_list


if __name__ == "__main__":
    config = readConfig()
    print(config)
    q_value = Counter()

    for i in range(10000):
        # view = NoGraphic()
        view = GameView(2)
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
