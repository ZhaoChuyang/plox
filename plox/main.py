import argparse
from plox.engine import run_script, run_promt
from plox import utils


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="Specify the plox script file path.", default="")
    return parser.parse_args()


def main():
    """
    Main entrance to launch the plox intepreter. You can run plox in two mode:
    1. run plox using script file.
    2. run plox in command line.
    """
    args = get_args()

    if args.file:
        run_script(args.file)
    else:
        run_promt()


if __name__ == '__main__':
    main()
