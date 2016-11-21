# Parses a Sudoku board from a given text file. Expects files of the
# following format:
# 9 total lines (one for each row of the board)
# Each line contains 9 "slots," with spaces between each of them
# Each "slot" contains either a number (for a clue) or a dash ("-"),
# meaning there is no clue for that "slot."
#
# Example:
# - - - 7 - - - - -
# 1 - - - - - - - -
# - - - 4 3 - 2 - -
# - - - - - - - - 6
# - - - 5 - 9 - - -
# - - - - - - 4 1 8
# - - - - 8 1 - - -
# - - 2 - - - - 5 -
# - 4 - - - - 3 - -
def parse_board_from_file(filename):
    f = open(filename, 'r')
    matrix = [[0 for x in range(0,9)] for y in range(0,9)]
    for x in range(0,9):
        row = f.readline()
        row_list = row.split()
        assert(len(row_list) == 9)
        for y in range(0,9):
            if row_list[y].isdigit():
                matrix[x][y] = int(row_list[y])
            else:
                matrix[x][y] = None

    return matrix
