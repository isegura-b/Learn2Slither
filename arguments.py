import argparse

def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("sessions must be greater than zero")
    return number


def build_parser():
    parser = argparse.ArgumentParser( description="Train or evaluate the Learn2Slither agent.")
    parser.add_argument(
        "-sessions",
        "--sessions",
        type=positive_int,
        default=1,
        help="number of games to run (default: 1)"
    )
    parser.add_argument(
        "-save",
        "--save",
        metavar="PATH",
        help="save the final learning state to PATH"
    )
    parser.add_argument(
        "-load",
        "--load",
        metavar="PATH",
        help="load a learning state before running"
    )
    parser.add_argument(
        "-visual",
        "--visual",
        choices=("on", "off"),
        default="on",
        help="enable or disable the graphical window (default: on)"
    )
    parser.add_argument(
        "-dontlearn",
        "--dontlearn",
        action="store_true",
        help="evaluate without changing the Q-table or epsilon values"
    )
    parser.add_argument(
        "-step-by-step",
        "--step-by-step",
        action="store_true",
        help="wait for Space or Enter before each move (visual mode only)"
    )
    return parser
