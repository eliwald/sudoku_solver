Solves n-by-n Sudoku puzzles. Usage:

python main.py path-to-sudoku-puzzle.txt

Example sudoku puzzle input file:

\- \- \- 7 \- \- \- \- \-  
1 \- \- \- \- \- \- \- \-  
\- \- \- 4 3 \- 2 \- \-  
\- \- \- \- \- \- \- \- 6  
\- \- \- 5 \- 9 \- \- \-  
\- \- \- \- \- \- 4 1 8  
\- \- \- \- 8 1 \- \- \-  
\- \- 2 \- \- \- \- 5 \-  
\- 4 \- \- \- \- 3 \- \-  

Alternatively, if you'd like to include the SudokuBoard class in your
own application, just use the `models` module:

```python
from models import SudokuBoard

# "matrix" should be an n-by-n array, with each entry either being an
# integer (representing a clue in the initial board) or None
# (representing an empty square in the initial baord)
matrix = ...
sudoku_board = SudokuBoard(matrix)
# Will return True if a valid solution is found, and False
# otherwise. After this call, sudoku_board will be completely filled in.
sudoku_board.solve()
```
