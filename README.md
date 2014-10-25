Sudoku-Solver
=============
In this problem, we solve Sudoku puzzles. Starting with backtracking, you will need to add MRV heuristic + forward checking +
arc consistency to the algorithm. You can write your own stand-alone program in any programming languages you like. Or you
can implement a provided Python function.
The code for this project contains the following files:
puzzle.txt :  Get to know the format of the input Sudoku.
sudokuSolver.py : The main file that solves the Sudoku puzzle. If you want to do use Python for this problem, you will fill out the solve_puzzle function.
solution.txt : The output of sudokuSolver.py.
sudokuGenerator.py : This file generates a random input Sudoku: puzzle.txt
sudokuChecker.py : This file validates the output of the Sudoku solver: solution.txt
sudokuUtil.py : Contains some supporting functions.
Y
ou can run the following command in sequence to get an idea of the pipeline:
Generate a puzzle. Write the puzzle to puzzle.txt.
python sudokuGenerator.py
-------------------------
You can change the number of given digits in the puzzle (default 30):
python sudokuGenerator.py 45
-----------------------------
Read puzzle.txt and solve it. Write the solution to solution.txt
python sudokuSolver.py
----------------------
Read solution.txt and check it
python sudokuChecker.py
-----------------------
You have two options: write your only stand-alone program with any programming languages you like, or implement the solve_puzzle function in sudokuSolver.py.
If you are going to write your own program, your should ignore sudokuSolver.py completely and replace it with your own program.
You program should take puzzle.txt as the input file and write to solution.txt as output. Remember to check your solution by
sudokuChecker.py.
If you like to deal with Python, we've done the I/O part in sudokuSolver.py for you and you can focus on the algorithm. You can
also use data structures in util.py or add your utilities in sudokuSolver.py.

Question 1 :
===========
Implement the basic backtracking algorithm. Generate 10 random Sudokus with puzzle.txt and evaluate
the solver. Report the average and variance of the performance.

Question 2 :
============
Add minimum remaining values (MRV) heuristic + forward checking + arc consistency to the algorithm.
To make arc consistency simpler, you can trigger constraint propagation only when a variable with just one valid value left is
discovered. Generate 10 random Sudokus with puzzle.txt and evaluate it. Report the average and variance of the performance.
