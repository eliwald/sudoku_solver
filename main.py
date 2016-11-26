import sys
from parser import *
from models import *

USAGE_STR = "Usage: python main.py path-to-sudoku-board.txt"

# The main function simply takes the path to the sudoku board to solve
# as an argument. It then prints the unsolved board followed by the
# solved board.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print USAGE_STR
    else:
        matrix = parse_board_from_file(sys.argv[1])
        if matrix:
            sudoku_board = SudokuBoard(matrix)
            print "Input board:\n%s" % sudoku_board
            if sudoku_board.solve():
                print "Solved board:\n%s" % sudoku_board
            else:
                print "No solution found"
