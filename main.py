import sys
import pprint
from parser import *
from models import *

if __name__ == "__main__":
    unsolved_board = SudokuBoard(parse_board_from_file(sys.argv[1]))
    print unsolved_board
    board = unsolved_board.solve()
    print board
    print unsolved_board
