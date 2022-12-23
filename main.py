from multiprocessing import Pool
from queue import Queue
from typing import Optional

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
    parser.add_argument("-m", "--num-of-matches", action="store", type=int, default=1, help="If the value is greater than 1, -n is enabled automatically.")
    parser.add_argument("-p", "--parallel", action="store", type=int, default=1, help="The maximum number of processes allowed.")
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


def singleGame(settings) -> Optional[Player]:
    if settings.no_graphic:
        assert settings.Red != "MouseAgent", "MouseAgent (Red) is not allowed when graphic is turned off."
        assert settings.Black != "MouseAgent", "MouseAgent (Black) is not allowed when graphic is turned off."
        view = NoGraphic()
    elif settings.res4:
        view = GameView(4)
    elif settings.res2:
        view = GameView(2)
    else:
        view = GameView(1)
    red_agent = initAgent(Player.Red, settings.Red, view)
    black_agent = initAgent(Player.Black, settings.Black, view)
    model = GameModel(view, red_agent, black_agent, settings.time)
    return model.startApp()


if __name__ == "__main__":
    config = readConfig()
    if config.num_of_matches != 1:
        config.time = 0.0
        config.no_graphic = True
    print(config)

    executor = Pool(processes=config.parallel)
    result = executor.starmap(singleGame, [(config,)] * config.num_of_matches)
    print(f"{'<---------------- Result ---------------->':^42}")
    print(f"|{'Total matches (including RE)':>32}: {config.num_of_matches:>5} |")
    print(f"|{f'Red ({config.Red}) Win':>32}: {result.count(Player.Red):>5} |")
    print(f"|{f'Black ({config.Black}) Win':>32}: {result.count(Player.Black):>5} |")
    print(f"|{'Draw':>32}: {result.count(Player.Draw):>5} |")
    print(f"{'<---------------------------------------->':^42}")
