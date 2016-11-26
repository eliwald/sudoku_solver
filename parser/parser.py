# Parses a Sudoku board from a given text file. Expects files of the
# following format:
# n total lines (one for each row of the board)
# Each line contains n "slots," with spaces between each of them
# Each "slot" contains either a number (for a clue) or a dash ("-"),
# meaning there is no clue for that "slot." Note that any contiguous
# string of non-numbers is treated as a single empty square
# (i.e. equivalent to a dash "-").
#
# Example input (9x9 board):
# - - - 7 - - - - -
# 1 - - - - - - - -
# - - - 4 3 - 2 - -
# - - - - - - - - 6
# - - - 5 - 9 - - -
# - - - - - - 4 1 8
# - - - - 8 1 - - -
# - - 2 - - - - 5 -
# - 4 - - - - 3 - -
#
# If an invalid file or an invalid board is passed in, then None is returned.
def parse_board_from_file(filename):
    try:
        f = open(filename, 'r')
        # First check to make sure it's a valid board by ensuring each row
        # contains side_length number of values and ensuring the
        # it's a square. We also use this to determine the side_length
        # for filling the matrix of values.
        row_length = len(f.readline().split())
        side_length = 1
        row = f.readline()
        while len(row) > 0:
            if len(row.split()) != row_length:
                print "All rows in the input board must be the same length"
                f.close()
                return None
            side_length += 1
            row = f.readline()
        if row_length != side_length:
            print "There must be an equal number of rows and columns in the input board"
            f.close()
            return None

        # Now we've validated the dimensions of the board. Close and re-open the file so
        # we can parse the values and fill the matrix with the values
        # from the file.
        f.close()
        f = open(filename, 'r')
        matrix = [[0 for x in range(0, side_length)] for y in range(0, side_length)]
        for x in range(0, side_length):
            row = f.readline()
            row_list = row.split()
            assert(len(row_list) == side_length)
            for y in range(0, side_length):
                if row_list[y].isdigit():
                    if int(row_list[y]) > side_length:
                        print "Numbers must range from 1 to the length of the board"
                        f.close()
                        return None
                    matrix[x][y] = int(row_list[y])
                else:
                    matrix[x][y] = None
        f.close()
        return matrix
    except IOError:
        print "Please provide a valid filename to a file containing a sudoku board"
        return None
