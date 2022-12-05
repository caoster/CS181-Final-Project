import getopt
import sys

from ExampleAgent import ExampleAgent
from gameModel import GameModel
from gameView import GameView
from utils import Piece


def readConfig():
    default = [False]

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h2e:", ["help", "2res", "example="])
    except getopt.GetoptError as e:
        print(e)
        print("Use option -h for help.")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("""
Usage: python3 main.py [options]

Options and arguments:
-h                  Display this message.
--help              Display this message.
-2                  Use (more than) 2 times resolution, this option is Off by default.
--2res              Use (more than) 2 times resolution, this option is Off by default.
-e <arg>            Example, followed by argument.
--example <arg>     Example, followed by argument.
            """)
            sys.exit()
        elif opt in ("-2", "--2res"):
            default[0] = True
        elif opt in ("-e", "--example"):
            print(arg)
            print("Here is an example of adding command line arguments\n"
                  "An short option with argument should be added with colon (:)\n"
                  "An long option with argument should be added with equal (=)")
        else:
            print(f"Unknown parameter: {opt}, use option -h for help.")
            exit(123123)  # unreachable

    return default


if __name__ == "__main__":
    print(sys.argv)
    config = readConfig()

    red_agent = ExampleAgent(GameModel.RED)
    black_agent = ExampleAgent(GameModel.BLACK)
    v = GameView(config[0])
    m = GameModel(v, red_agent, black_agent)
    m.startApp()
