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

class Board:
    DIMS = (9, 9)
    __slots__ = ["nums", "white_dots", "black_dots"]

def no_dot_constraint(a, b): return True

def white_dot_constrant(a, b):
    return a == b + 1 or a + 1 == b

def black_dot_constraint(a, b):
    return a == b * 2 or a * 2 == b

# Checks that each row has exactly one of each digit 1 - 9
def check_row_constraint(nums):
    for row in nums:
        digit_count = [0] * 10
        for num in row:
            # Check if a digit other than zero is duplicated
            if num and digit_count[num]: return False
            digit_count[num] += 1

# Checks that each column has exactly one of each digit 1 - 9
def check_column_constraint(nums):
    for col in nums.T:
        digit_count = [0] * 10
        for num in col:
            # Check if a digit other than zero is duplicated
            if num and digit_count[num]: return False
            digit_count[num] += 1

# Checks that each 3x3 grid has exactly one of each digit 1 - 9
def check_grid_constraint(nums):
    # i, j in {0, 3, 6}
    # i and j are the top left indices of our 3x3 grid
    for i, j in product(range(0, 9, 3), repeat=2):
        digit_count = [0] * 10
        # m and n are the indices for our 3x3 grid
        for m, n in product(range(i, i + 3), range(j, j + 3)):
            # Check if a digit other than zero is duplicated
            if nums[i, j] and digit_count[nums[i, j]]: return False
            digit_count[nums[i, j]] += 1

# Checks the row, column, and grid constraints
def check_unique_constraint(nums):
    valid = True
    valid = valid and check_row_constraint(nums)
    valid = valid and check_column_constraint(nums)
    valid = valid and check_grid_constraint(nums)

    return valid

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

# i in [0, 9], j in [0, 8]
# Checks that the position at i, j satisfies all dot constraints
def check_dot_constraints(board, i, j):
    # Checking vertical dot constraints

    # A vertical dot at (i, j) applies constraints to
    # board positions (i, j) and (i, j + 1)
    if not Dot.CONSTRAINTS[board.vert_dots[i, j]](board[i, j], board[i, j + 1]):
        return False
    
    # Checking horizontal dot constraints

    # A horizontal dot at (j, i) applies constraints to
    # board positions (j, i) and (j + 1, i)
    if not Dot.CONSTRAINTS[board.horiz_dots[j, i]](board[j, i], board[j + 1, i]):
        return False
    
    return True

# Checks if the given board satisfies the constraints
# specified by the dots
def is_valid_kropki(board: Board):
    # Checking row, column, and grid constraints for unique digits
    if not check_unique_constraint(board.nums):
        return False
    
    # We iterate over each position in the board, checking that each satisfies all constraints
    # i in [0, 9], j in [0, 8]
    for i, j in product(range(Board.DIMS[0]), range(Board.DIMS[1] - 1)):
        # Checking vertical dot constraints

        if not check_dot_constraints(board, i, j):
            return False
    
    return True

# Returns the number of valid values for i, j given the current board constraints
def count_valid_values(board, i, j) -> int:
    count = 0
    # possible in [1, 9]
    for possible in range(1, 10):
        

def select_square_to_fill(board):
    pass

def solve_kropki_board(board):
    if all(board.nums): return board # Complete assignment. Must be valid


def solve_kropki(file_name):
    # 9x9
    board = Board()
    board.nums = np.loadtxt(file_name, delimiter=' ', usecols=range(Board.DIMS[1]), max_rows=Board.DIMS[0])

    # 8x9
    board.vert_dots = np.loadtxt(
        file_name, delimiter=' ', skiprows=Board.DIMS[0] + 1, usecols=range(Board.DIMS[1] - 1), max_rows=Board.DIMS[0]
    )

    # 9x8
    board.horiz_dots = np.loadtxt(
        file_name, delimiter=' ', skiprows=Board.DIMS[0] * 2 + 2, usecols=range(Board.DIMS[1]), max_rows=Board.DIMS[0] - 1
    )

    solve_kropki_board(board)



def main():
    try:
        with open(sys.argv[1]) as file:
            solve_kropki(sys.argv[1])
    except Exception as exc:
        print(f"Failed to read file.")
        print(f"{exc}")

if __name__ == "__main__":
    main()