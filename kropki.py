# @file     kropki.py
# @author   Evan Brody
# @brief    Solves a Kropki Sudoku board

import os
import sys
import numpy as np
from itertools import product, chain
from copy import deepcopy

# Vertical dot: |
#               O
#               |
# Horizontal dot: -o-

def no_dot_constraint(a, b): return True

def white_dot_constrant(a, b):
    return a == b + 1 or a + 1 == b

def black_dot_constraint(a, b):
    return a == b * 2 or a * 2 == b

# Checks that each digit 1 - 9 is only used once within the array
def array_all_diff(array):
    digit_count = [0] * 10
    for num in array:
        # Check if a digit other than zero is duplicated
        if num and digit_count[num]: return False
        digit_count[num] += 1
    
    return True

# Checks that the AllDiff constraint is satisfied at row i
def check_row_constraint_at(nums, i):
    return array_all_diff(nums[i])

# Checks that the AllDiff constraint is satisfied at column j
def check_column_constraint_at(nums, j):
    return array_all_diff(nums.T[j])

# Checks that the grid AllDiff constraint is satisfied for the
# grid that contains position m, n
def check_grid_constraint_at(nums, m, n):
    # Indices m, n are in grid index m div 3, n div 3
    i, j = m // 3, n // 3
    i *= 3; j *= 3 # Starting indices for that grid (top-left)

    digit_count = [0] * 10
    for ii, jj in product(range(i, i + 3), range(j, j + 3)):
        # Check if a digit other than zero is duplicated
        if nums[ii, jj] and digit_count[nums[ii, jj]]: return False
        digit_count[nums[ii, jj]] += 1

    return True

class Board:
    __slots__ = ["nums", "vert_dots", "horiz_dots"]

    DIMS = (9, 9)
    NO_DOT = 0
    WHITE_DOT = 1
    BLACK_DOT = 2
    # When indexed at *_DOT, this triple
    # returns the constraint associated with
    # that dot
    DOT_CONSTRAINTS = (
        no_dot_constraint,
        white_dot_constrant,
        black_dot_constraint
    )

    def __init__(self, nums, vert_dots, horiz_dots):
        self.nums = nums
        self.vert_dots = vert_dots
        self.horiz_dots = horiz_dots

def check_unique_constraints_at(nums, i, j):
    if not check_row_constraint_at(nums, i):
        return False
    
    if not check_column_constraint_at(nums, j):
        return False
    
    if not check_grid_constraint_at(nums, i, j):
        return False
    
    return True

def check_dot_constraints_at(board, i, j):
    # A number at position i, j is constrained by dots at indices
    # LEFT: i, j - 1; RIGHT: i, j (vertical dots)
    # UP:   i - 1, j; DOWN:  i, j (horizontal dots)
    
    # Checking left
    if j - 1 > 0 and board.nums[i, j - 1]:
        if not Board.DOT_CONSTRAINTS[board.vert_dots[i, j - 1]](
            board.nums[i, j], board.nums[i, j - 1]
        ):
            return False

    # Checking right
    if j + 1 < Board.DIMS[1] and board.nums[i, j + 1]:
        if not Board.DOT_CONSTRAINTS[board.vert_dots[i, j]](
            board.nums[i, j], board.nums[i, j + 1]
        ):
            return False
    
    # Checking top
    if i - 1 > 0 and board.nums[i - 1, j]:
        if not Board.DOT_CONSTRAINTS[board.horiz_dots[i - 1, j]](
            board.nums[i, j], board.nums[i - 1, j]
        ):
            return False

    # Checking bottom
    if i + 1 < Board.DIMS[0] and board.nums[i + 1, j]:
        if not Board.DOT_CONSTRAINTS[board.horiz_dots[i, j]](
            board.nums[i, j], board.nums[i + 1, j]
        ):
            return False
    
    return True

# Checks if the assignment at i, j is valid
def is_valid_at(board, i, j):
    if not check_dot_constraints_at(board, i, j):
        return False
    
    if not check_unique_constraints_at(board.nums, i, j):
        return False
    
    return True

# Returns the degree of position i, j
# i.e., the number of unassigned variables i, j constrains
def get_degree(board, i, j):
    if board.nums[i, j]:
        raise Exception("get_degree() called on assigned variable.")
    
    degree = 0

    # A number at position i, j is constrained by dots at indices
    # LEFT: i, j - 1; RIGHT: i, j (vertical dots)
    # UP:   i - 1, j; DOWN:  i, j (horizontal dots)
    if j - 1 > 0: # Ensure index within range
        # Left vertical dot
        # If there is a vertical dot to the left, and the position
        # to the left is unassigned
        if board.vert_dots[i, j - 1] and not board.nums[i, j - 1]:
            degree += 1
    
    if j + 1 < Board.DIMS[1]:
        # Right vertical dot
        # If there is a vertical dot to the right, and the position
        # to the left is unassigned
        if board.vert_dots[i, j] and not board.nums[i, j + 1]:
            degree += 1
    
    if i - 1 > 0:
        # Upper horizontal dot
        # If there is a horizontal dot above, and the position
        # above is unassigned
        if board.horiz_dots[i - 1, j] and not board.nums[i - 1, j]:
            degree += 1
    
    if i < Board.DIMS[0] - 1:
        # Lower horizontal dot
        # If there is a horizontal dot below, and the position
        # below is unassigned
        if board.horiz_dots[i, j] and not board.nums[i, j]:
            degree += 1

    return degree

def get_valid_domain(board, i, j):
    if board.nums[i, j]:
        raise Exception("Domain requested for assigned variable.")
    
    final_valid = set(range(1, 10))
    for number in range(1, 10):
        board.nums[i, j] = number
        if not is_valid_at(board, i, j):
            final_valid.remove(number)
    
    board.nums[i, j] = 0
    return final_valid

# Returns the number of valid values for i, j given the current board constraints
def count_valid_values(board, i, j) -> int:
    return len(get_valid_domain(board, i, j))

def select_square_to_fill(board):
    selections = []

    # Start with Minimum Remaining Values heuristic
    selection_value_count = 10 # Each position can have, at most, 9 valid values
    for i, j in product(range(0, 9), repeat=2):
        if not board.nums[i, j]:
            ij_value_count = count_valid_values(board, i, j)
            if ij_value_count < selection_value_count:
                selection_value_count = ij_value_count
                selections = [(i, j)]
            elif ij_value_count == selection_value_count:
                selections.append((i, j))

    # Tiebreak via degree heuristic (highest degree is selected)
    # Final selection is not an array because we arbitrarily choose from variables with equal degree
    final_selection = None
    max_degree = -1
    for coord in selections:
        coord_degree = get_degree(board, *coord)
        if coord_degree > max_degree:
            max_degree = coord_degree
            final_selection = coord
    
    # Arbitrary final tiebreak
    return final_selection

# Forward check detects some early failures (empty domain)
# after an assignment to position i, j
def forward_check(board, i, j):    
    # First check variables in the same grid
    grid_i, grid_j = (i // 3) * 3, (j // 3) * 3
    for ii, jj in product(range(grid_i, grid_i + 3), range(grid_j, grid_j + 3)):
        if not board.nums[ii, jj] and not count_valid_values(board, ii, jj):
            return False

    # Then in the same column, excluding the grid
    # Hold j fixed, vary ii
    for ii in chain(range(0, grid_i), range(grid_i + 3, board.nums.shape[0])):
        if not board.nums[ii, j] and not count_valid_values(board, ii, j):
            return False

    # Then in the same row, excluding the grid
    # Hold i fixed, vary jj
    for jj in chain(range(0, grid_j), range(grid_j + 3, board.nums.shape[1])):
        if not board.nums[i, jj] and not count_valid_values(board, i, jj):
            return False
        
    return True

def solve_kropki_board(board):
    os.system("cls")
    print(board.nums)
    if board.nums.all(): return board # Complete assignment. Must be valid
    var = select_square_to_fill(board) # var is a tuple (i, j)
    for value in get_valid_domain(board, *var):
        board.nums[var] = value
        if True or forward_check(board, *var): # Inference
            result = solve_kropki_board(deepcopy(board))
            if type(result) != bool: return result # False indicates failure
        
        board.nums[var] = 0 # Clear the assignment
    
    return False

def solve_kropki(file_name):
    # 9x9
    nums = np.loadtxt(
        file_name, dtype=int, delimiter=' ', usecols=range(Board.DIMS[1]), max_rows=Board.DIMS[0]
    )

    # 9x8
    vert_dots = np.loadtxt(
        file_name, dtype=int, delimiter=' ', skiprows=Board.DIMS[0] + 1, usecols=range(Board.DIMS[1] - 1), max_rows=Board.DIMS[0]
    )

    # 8x9
    horiz_dots = np.loadtxt(
        file_name, dtype=int, delimiter=' ', skiprows=Board.DIMS[0] * 2 + 2, usecols=range(Board.DIMS[1]), max_rows=Board.DIMS[0] - 1
    )

    solved = solve_kropki_board(Board(nums, vert_dots, horiz_dots))
    if solved is False:
        print("FAILURE")
        return
    
    name, ext = file_name.split('.')
    ext = '.' + ext
    with open("Output" + name[-1] + ext, 'w') as output_file:
        # Text processing
        output_str = np.array2string(solved.nums) # Convert array to string
        output_str = output_str.translate({ord(c) : None for c in "[]"}) # Remove array delimiters
        output_str = '\n'.join([ line.strip() for line in output_str.splitlines() ]) # Strip spaces from each line

        output_file.write(output_str)

if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as file:
            solve_kropki(sys.argv[1])
    except Exception as exc:
        print(f"Failed to read file.")
        print(f"{exc}")