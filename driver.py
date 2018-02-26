#!/usr/bin/env python3

import sys
from timeit import default_timer

# local imports
from puzzle import Puzzle
from tree import Tree


def main(puzzle_file):
    """Main function of our program's driver. Times execution and prints results.

    Args:
        puzzle_file: The name of the input file describing the puzzle.
    """

    try:
        with open(puzzle_file) as f:
            puzzle_file = f.read()
    except IOError as e:
        sys.exit(e)

    print(puzzle_file.strip())      # print input file
    start_time = default_timer()    # begin timer

    puzzle_file = puzzle_file.splitlines()

    try:
        # unpack puzzle init values, then pass the remainder as the board
        tree = Tree(Puzzle(*puzzle_file[:7], puzzle_file[7:]))
    except (TypeError, ValueError) as e:
        sys.exit(e)

    # perform A* graph search and print results
    print(tree.astargs())
    print(default_timer() - start_time)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: {} puzzle_file".format(sys.argv[0]))
