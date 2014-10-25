# SUDOKU SOLVER
import copy
import sys
from time import time
from sudokuUtil import *

# Please implement function solve_puzzle
# input puzzle: 2D list, for example:
# [ [0,9,5,0,3,2,0,6,4]
#   [0,0,0,0,6,0,1,0,0]
#   [6,0,0,0,0,0,0,0,0]
#   [2,0,0,9,0,3,0,0,6]
#   [0,7,6,0,0,0,0,0,3]
#   [3,0,0,0,0,0,0,0,0]
#   [9,0,0,5,0,4,7,0,1]
#   [0,5,0,0,2,1,0,9,0]
#   [0,0,8,0,0,6,3,0,5] ]
# Return a 2D list with all 0s replaced by 1 to 9.
# You can utilize argv to distinguish between algorithms
# (basic backtracking or with MRV and forward checking).
# For example: python sudokuSolver.py backtracking


# Checks if the returned solution is a valid solution
def checkSolution(sudoku):
  if len(sudoku) != 9:
    return False

  # Checking rows, columns and cubes one by one for a valid solution
  # Check rows
  for i in sudoku:
    # Sort the row and check if numbers are from 1 to 9
    if sorted(i) != [1,2,3,4,5,6,7,8,9]:
      return False

  # Check columns
  for i in range(9):
    tempSudoku = []
    for j in range(9):
      tempSudoku.append(sudoku[j][i])
    # Sort the column and check if numbers are from 1 to 9
    if sorted(tempSudoku) != [1,2,3,4,5,6,7,8,9]:
      return False

  # Check cubes
  for i in range(3):
    for j in range(3):
      tempSudoku = sudoku[i*3][j*3:j*3+3] + sudoku[i*3+1][j*3:j*3+3] + sudoku[i*3+2][j*3:j*3+3]
      # Sort all numbers in cube and check if numbers are from 1 to 9
      if sorted(tempSudoku) != [1,2,3,4,5,6,7,8,9]:
        return False

  return True

def solve_puzzle(puzzle, start):
  """Solve the sudoku puzzle."""
  # Initializing the list to store solutions
  solutions = []
  
  # Basic backtracking algorithm
  for i in range(9):
    for j in range(9):
      # If the entry is blank then proceed further	
      if puzzle[i][j] == 0:
        for k in range(1,10):
	  # Checking if that number(which is k here) is present in same row or same column or same cube
	  # If yes then move to the next number
	  # Same Row: puzzle[i]
          # Same Column: [row[j] for row in puzzle]
	  # Same Cube: puzzle[i//3*3][j//3*3:j//3*3+3] + puzzle[i//3*3+1][j//3*3:j//3*3+3] + puzzle[i//3*3+2][j//3*3:j//3*3+3]
          if (k in puzzle[i] or k in [row[j] for row in puzzle] or k in (puzzle[i//3*3][j//3*3:j//3*3+3] + puzzle[i//3*3+1][j//3*3:j//3*3+3] + puzzle[i//3*3+2][j//3*3:j//3*3+3])):
	    continue	
          else:  
	    # Copying the puzzle to temporary variable each time
	    tempSudoku = copy.deepcopy(puzzle)
            # Assigning k to tempSudoku[i][j]
	    tempSudoku[i][j] = k
	    # Recursive Call
            solution = solve_puzzle(tempSudoku, False)
            if solution != None:
              solutions.append(solution)

        # Check if each solution is a valid solution
	for solution in solutions:
          if checkSolution(solution):
            return solution
        return None

  # Checking if the puzzle itself is solved
  if checkSolution(puzzle):
    return puzzle
  return None

#===================================================#
puzzle = load_sudoku('puzzle.txt')

print "solving ..."
t0 = time()
solution = solve_puzzle(puzzle,True)
t1 = time()
print "completed. time usage: %f" %(t1 - t0), "secs."

save_sudoku('solution.txt', solution)

