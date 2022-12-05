import getopt
import sys

from ExampleAgent import ExampleAgent
from gameModel import GameModel
from gameView import GameView


def readConfig():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--res2", action="store_true", help="Use (more than) 2 times resolution, this option is Off by default.")
    parser.add_argument("-e", "--example", nargs="*", type=str, default=None, help="Example, followed by argument.")
    args = parser.parse_args()
    if args.example != None:
        print(args.example)
        print("Here is an example of adding command line arguments")
    # print(args)
    return args


if __name__ == "__main__":
    print(sys.argv)
    config = readConfig()

    red_agent = ExampleAgent(GameModel.RED)
    black_agent = ExampleAgent(GameModel.BLACK)
    v = GameView(config.res2)
    m = GameModel(v, red_agent, black_agent)
    m.startApp()
