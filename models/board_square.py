# A class representing a single square in
class BoardSquare(object):
    # The default number we use if the number for a given square hasn't
    # been set yet
    default_num = 0

    def __init__(self, row, col):
        # Initialize the square at this row and column
        self.row = row
        self.col = col

        # Initialize the number at this index to be the default (which
        # indicates that we don't know what number goes here yet)
        self.num = BoardSquare.default_num

        # Initialize the helper data structures that we'll use to keep
        # track of what numbers may go here
        self.possible_nums = []

    # Used when sorting BoardSquares in a heap in the solver. A
    # BoardSquare will be less than another BoardSquare if it has
    # fewer possible numbers that can be put in it.
    def __lt__(self, other):
        return len(self.possible_nums) < len(other.possible_nums)

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
