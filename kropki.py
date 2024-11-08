# @file kropki.py
# @author Evan Brody
# @brief Solves a Kropki Sudoku board

import sys
import random
import numpy as np
from itertools import product

# Vertical dot: |
#               O
#               |
# Horizontal dot: -o-

BOARD_DIMS = (9, 9)

def no_dot_constraint(a, b): return True

def white_dot_constrant(a, b):
    return a == b + 1 or a + 1 == b

def black_dot_constraint(a, b):
    return a == b * 2 or a * 2 == b

class Dot:
    NO_DOT = 0
    WHITE_DOT = 1
    BLACK_DOT = 2
    # When indexed at *_DOT, this triple
    # returns the constraint associated with
    # that dot
    CONSTRAINTS = (
        no_dot_constraint,
        white_dot_constrant,
        black_dot_constraint
    )

# Checks if the given board satisfies the constraints
# specified by the dots
def is_valid_kropki(board, vert_dots, horiz_dots):
    # We iterate over the constraints, checking if the board satisfies all
    # i in [0, 9], j in [0, 8]
    for i, j in product(range(BOARD_DIMS[0]), range(BOARD_DIMS[1] - 1)):
        # Checking vertical dot constraints

        # A vertical dot at (i, j) applies constraints to
        # board positions (i, j) and (i, j + 1)
        if not Dot.CONSTRAINTS[vert_dots[i, j]](board[i, j], board[i, j + 1]):
            return False
        
        # Checking horizontal dot constraints

        # A horizontal dot at (j, i) applies constraints to
        # board positions (j, i) and (j + 1, i)
        if not Dot.CONSTRAINTS[horiz_dots[j, i]](board[j, i], board[j + 1, i]):
            return False
    
    return True

def count_valid_values(board, i, j):
    

def select_square_to_fill(board):
    

def solve_kropki_board(board, vert_dots, horiz_dots):
    if all(board): return board # Complete assignment. Must be valid




def solve_kropki(file_name):
    # 9x9
    board = np.loadtxt(file_name, delimiter=' ', usecols=range(BOARD_DIMS[1]))

    # 8x9
    vert_dots = np.loadtxt(
        file_name, delimiter=' ', skiprows=BOARD_DIMS[0], usecols=range(BOARD_DIMS[1] - 1)
    )

    # 9x8
    horiz_dots = np.loadtxt(
        file_name, delimiter=' ', skiprows=BOARD_DIMS[0]*2, usecols=range(BOARD_DIMS[1])
    )




def main():
    try:
        with open(sys.argv[1]) as file:
            solve_kropki(sys.argv[1])
    except Exception as exc:
        print(f"Failed to read file.")
        print(f"{exc}")
    solve_kropki(sys.argv[1])

if __name__ == "main":
    main()