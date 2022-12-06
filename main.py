from ExampleAgent import ExampleAgent
from gameModel import GameModel
from gameView import GameView
from utils import Side


def readConfig():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--res2", action="store_true", help="Use (more than) 2 times resolution, this option is OFF by default.")
    parser.add_argument("-t", "--time", action="store", type=float, default=1.0, help="The time interval in seconds between calling step functions, default interval is 1.0 second.")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    config = readConfig()
    print(config)

    red_agent = ExampleAgent(Side.Red)
    black_agent = ExampleAgent(Side.Black)
    v = GameView(config.res2)
    m = GameModel(v, red_agent, black_agent, config.time)
    m.startApp()
