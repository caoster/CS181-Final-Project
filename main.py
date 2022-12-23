from queue import Queue

from ExampleAgent import ExampleAgent
from HumanPlayer.mouseAgent import MouseAgent
from Adversarial.MinimaxAgent import MinimaxAgent
from agent import Agent
from gameModel import GameModel
from gameView import GameView, NoGraphic
from utils import Player
from MCTS.MCTSAgent import MCTSAgent


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
    args = parser.parse_args()
    return args


def initAgent(side: Player, choice: str, relate_view: GameView) -> Agent:
    if choice == "MouseAgent":
        agent = MouseAgent(side)
        tunnel = Queue(1)
        agent.setTunnelIn(tunnel)
        relate_view.enableMouse(side, tunnel)
    elif choice == "ExampleAgent":
        agent = ExampleAgent(side)
    elif choice == "MinimaxAgent":
        agent = MinimaxAgent(side)
    elif choice == "MCTSAgent":
        agent = MCTSAgent(side)
    else:
        assert False, "No such agent!"
    return agent


if __name__ == "__main__":
    config = readConfig()
    print(config)

    if config.no_graphic:
        assert config.Red != "MouseAgent", "MouseAgent (Red) is not allowed when graphic is turned off."
        assert config.Black != "MouseAgent", "MouseAgent (Black) is not allowed when graphic is turned off."
        view = NoGraphic()
    elif config.res4:
        view = GameView(4)
    elif config.res2:
        view = GameView(2)
    else:
        view = GameView(1)
    red_agent = initAgent(Player.Red, config.Red, view)
    black_agent = initAgent(Player.Black, config.Black, view)
    model = GameModel(view, red_agent, black_agent, config.time)
    model.startApp()
