from board_square import BoardSquare
from heapq import *

class SudokuBoard(object):
    def __init__(self, sudoku_matrix=[[BoardSquare.default_num for x in range(0,9)] for y in range(0,9)]):
        # Matrix of BoardSquare objects
        self.board = [[BoardSquare(y, x) for x in range(0, 9)] for y in range(0,9)]

        # Maintain a hashmap from octant to a list of board squares in
        # that octant
        self.octant_map = {}
        for x in range(0, 9):
            self.octant_map[x] = []

        # Initialize the sudoku board from input
        for row in range(len(sudoku_matrix)):
            for col in range(len(sudoku_matrix[0])):
                square = self.board[row][col]
                square.num = sudoku_matrix[row][col] if sudoku_matrix[row][col] else BoardSquare.default_num
                # Figure out which octant this square is in
                self.octant_map[self.octant_for_square(square)].append(square)

    # Return the octant that a given square is in. Octants are
    # numbered 0 through 8, counting left-to-right, top-to-bottom,
    # starting in the upper-left-hand-corner. Each octant contains 9 squares.
    def octant_for_square(self, square):
        return 3*(square.row/3) + square.col/3

    # Returns a list of squares in the given row
    def get_row(self, row):
        return self.board[row]

    # Returns a list of squares in the same row as the given square
    def get_row_for_square(self, square):
        return self.board[square.row]

    # Returns a list of squares in the given column
    def get_col(self, col):
        return [row[col] for row in self.board]

    # Returns the list of squares in the same column as the given square
    def get_col_for_square(self, square):
        return [row[square.col] for row in self.board]

    # Returns the list of squares in the same octant as the given square
    def get_octant_for_square(self, square):
        return self.octant_map[self.octant_for_square(square)]

    # Returns a list of possible numbers for a given square
    def get_possible_numbers_for_square(self, square):
        # If this square already is assigned a number, then that is
        # the only possible number it could be
        if square.num != BoardSquare.default_num:
            return [square.num]
        else:
            # Get all the numbers in the same row, column, and octant
            # as this square, and return the list of numbers that are
            # *not* in any of those lists.
            row_nums = [sq.num for sq in self.get_row_for_square(square)]
            col_nums = [sq.num for sq in self.get_col_for_square(square)]
            oct_nums = [sq.num for sq in self.get_octant_for_square(square)]
            possible_nums = []
            for x in range(1, 10):
                if x not in row_nums and x not in col_nums and x not in oct_nums:
                    possible_nums.append(x)
            return possible_nums

    # Updates the possible_nums attribute for all squares in the board
    def generate_possible_nums_for_each_square(self):
        for row in self.board:
            for square in row:
                square.possible_nums = self.get_possible_numbers_for_square(square)

    # Solves the Sudoku
    def solve(self):
        h = []
        # Generate the list of possible values for each square
        self.generate_possible_nums_for_each_square()
        # Push all non-set squares into the heap
        for row in self.board:
            for square in row:
                if square.num == BoardSquare.default_num:
                    heappush(h, square)

        # If we don't have any squares in the queue, that means we're
        # done (every square has been set)
        if len(h) == 0:
            return True
        # If the next item in the heap has no possibilities, then
        # we've reached an impossible state (return false)
        elif len(h[0].possible_nums) == 0:
            return False
        else:
            # Get the square with the least possible numbers off the
            # top of the heap
            sq = heappop(h)
            # If there's only one possible number for this square, set
            # it and recurse
            if len(sq.possible_nums) == 1:
                sq.num = sq.possible_nums[0]
                if self.solve():
                    return True
                else:
                    # Make sure to reset the square's number if this
                    # branch of the recursive tree doesn't work
                    sq.num = BoardSquare.default_num
                    return False
            # Otherwise, try all the possible numbers for this square
            # in succession. As soon as we find one that solves the
            # board, return up.
            else:
                # Make sure to copy the values out of
                # sq.possible_nums, since sq.possible_nums may get
                # changed in subsequent recursive calls
                possible_nums_to_try = list(sq.possible_nums)
                for i in range(0, len(possible_nums_to_try)):
                    sq.num = possible_nums_to_try[i]
                    if self.solve():
                        return True
                # If none of these numbers worked, then this branch of
                # the recursive tree must be invalid. Return False up,
                # and make sure to reset the value of the square.
                sq.num = BoardSquare.default_num
                return False

    # Print the board (for debugging purposes)
    def __str__(self):
        to_ret = ""
        for row in self.board:
            for sq in row:
                to_ret += "%d " % sq.num
            to_ret += "\n"

        return to_ret
