from board_square import BoardSquare
from heapq import *

# The default side length of a Sudoku board
DEFAULT_SIDE_LEN = 9

# Class representing a Sudoku board. A Sudoku board is comprised of a
# n-by-n array of SudokuSquare objects (each SudokuSquare object represents
# a square on the Sudoku board).
class SudokuBoard(object):
    # Takes as input a parsed n-by-n array, which is then converted
    # into the internal representation of the board. If no board is
    # passed in, an empty board with length DEFAULT_SIDE_LEN is
    # created
    # by default.
    def __init__(self, sudoku_matrix=[[BoardSquare.default_num for x in range(0, DEFAULT_SIDE_LEN)] for y in range(0, DEFAULT_SIDE_LEN)]):
        side_len = len(sudoku_matrix)
        # Matrix of BoardSquare objects, which will be populated by
        # the input sudoku_matrix.
        self.board = [[BoardSquare(y, x) for x in range(0, side_len)] for y in range(0, side_len)]

        # Maintain a hashmap from the index of a 3x3 section (counting
        # top-to-bottom and left-to-right) to the squares contained in
        # that section. This will be used later to help check board validity
        self.__section_map = {}
        for x in range(0, side_len):
            self.__section_map[x] = []

        # Initialize the sudoku board from input
        for row in range(side_len):
            for col in range(side_len):
                square = self.board[row][col]
                square.num = sudoku_matrix[row][col] if sudoku_matrix[row][col] else BoardSquare.default_num
                # Figure out which section this square is in, and add
                # this square to the list of squares in that section
                self.__section_map[self.__section_for_square(square)].append(square)

    # Return the section that a given square is in. Sections are
    # numbered 0 through (board_len - 1), counting left-to-right, top-to-bottom,
    # starting in the upper-left-hand-corner. Each section contains 9 squares.
    def __section_for_square(self, square):
        return 3*(square.row/3) + square.col/3

    # Returns a list of squares in the same row as the given square
    def __get_row_for_square(self, square):
        return self.board[square.row]

    # Returns the list of squares in the same column as the given square
    def __get_col_for_square(self, square):
        return [row[square.col] for row in self.board]

    # Returns the list of squares in the same octant as the given square
    def __get_section_for_square(self, square):
        return self.__section_map[self.__section_for_square(square)]

    # Sets the "possible_nums" variable for the given square by
    # populating it with the list of numbers this square could
    # possibly contain
    def __set_possible_numbers_for_square(self, square):
        # If this square already is assigned a number, then that is
        # the only possible number it could be
        if square.num != BoardSquare.default_num:
            square.possible_nums = [square.num]
        else:
            # Get all the numbers in the same row, column, and section
            # as this square, and return the list of numbers that are
            # *not* in any of those lists.
            row_nums = [sq.num for sq in self.__get_row_for_square(square)]
            col_nums = [sq.num for sq in self.__get_col_for_square(square)]
            oct_nums = [sq.num for sq in self.__get_section_for_square(square)]
            possible_nums = []
            for x in range(1, 10):
                if x not in row_nums and x not in col_nums and x not in oct_nums:
                    possible_nums.append(x)
            square.possible_nums = possible_nums

    # Updates the possible_nums attribute for all squares in the board
    def __generate_possible_nums_for_each_square(self):
        for row in self.board:
            for square in row:
                self.__set_possible_numbers_for_square(square)

    # Solves the Sudoku board. After calling this method, if the board
    # has a valid solution, all the SudokuSquares in the board will be
    # filled in. The function is recursive, and returns "True" if a
    # solution was found and "False" if no solution was found.
    def solve(self):
        # h is a heap of BoardSquares. The top of the heap contains
        # the BoardSquare with the least possible numbers that could
        # go in that square. We will pop off the heap to fill in that
        # square before recurring.
        h = []

        # Generate the list of possible values for each square in the board
        self.__generate_possible_nums_for_each_square()

        # Push all squares into the heap that haven't already been
        # filled in
        for row in self.board:
            for square in row:
                if square.num == BoardSquare.default_num:
                    heappush(h, square)

        # If we don't have any squares in the heap, that means we're
        # done (every square has been set)
        if len(h) == 0:
            return True

        # If the next item in the heap has no possibilities, then
        # we've reached an impossible state (return False)
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
                # If the recursive call to self.solve() returned True,
                # that means a solution was found. Return True up the
                # recursive tree. If the recursive call to
                # self.solve() returned False, that means a solution
                # wasn't found in this branch of the recursive
                # tree. Return False to indicate that this branch
                # doesn't contain a valid solution, resetting the
                # square's value back to empty.
                if self.solve():
                    return True
                else:
                    sq.num = BoardSquare.default_num
                    return False
            # If there are several possible numbers for this square,
            # try them all in succession. As soon as we find one that solves the
            # board, return True up to the recursive tree to indicate
            # we've found a solution.
            else:
                # Make sure to copy the values out of
                # sq.possible_nums, since sq.possible_nums may get
                # changed in subsequent recursive calls between
                # iterations of the below loop
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

    # Print the board
    def __str__(self):
        to_ret = ""
        for row in self.board:
            for sq in row:
                to_ret += "%d " % sq.num
            to_ret += "\n"

        return to_ret
