# A class representing a single square in a Sudoku board. Each Square
# contains it's row and column. It also contains it's number if it's
# been set, and a list that can be filled with possible numbers for
# this square if it's number hasn't been set.
class BoardSquare(object):
    # The default number we use if the number for a given square hasn't
    # been set yet.
    default_num = 0

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.num = BoardSquare.default_num
        self.possible_nums = []

    # Used when sorting BoardSquares in a heap in SudokuBoard.solve. A
    # BoardSquare is "less than"" another BoardSquare if it has
    # fewer possible numbers that can be put in it.
    def __lt__(self, other):
        return len(self.possible_nums) < len(other.possible_nums)

    # Prints the state of a BoardSquare (for debugging purposes)
    def __str__(self):
        board_square_str = "%d, %d: " % (self.row, self.col)
        if self.num == BoardSquare.default_num:
            board_square_str += "No number yet."
            if len(self.possible_nums) > 0:
                board_square_str += " Possible numbers:"
                for n in self.possible_nums:
                    board_square_str += " %d" % n
            else:
                board_square_str += " No possible numbers."
        else:
            board_square_str += "%d" % self.num
        return board_square_str
