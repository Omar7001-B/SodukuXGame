# Sudoku Solver

This project is a Sudoku solver and generator implemented in Python using Pygame. It allows users to play, solve, and get hints for Sudoku puzzles.

## Features

- **Random Sudoku Generation**: Generates a new Sudoku board with a random configuration.
- **Manual Solving**: Allows users to solve the puzzle manually.
- **Hint System**: Provides hints to the user.
- **Visual Solver**: Shows the step-by-step process of solving the Sudoku puzzle.

## Getting Started

### Running the Game

Run the main script to start the Sudoku game:
```bash
pip install pygame
python main.py
```

## How to Play

- Click on a cell to select it.
- Use the number keys (1-9) to input a value.
- Press `BACKSPACE` to remove a value.
- Press `ENTER` to confirm a value.
- Press `H` for a hint.
- Press `SPACE` to automatically solve the puzzle.

## Algorithms Used

### Backtracking Algorithm

The main algorithm used for solving the Sudoku puzzle is the backtracking algorithm. This is a depth-first search algorithm that incrementally builds candidates for the solutions and abandons each candidate ("backtracks") as soon as it determines that the candidate cannot lead to a valid solution.

#### How It Works

1. **Find an empty cell**: The algorithm searches for an empty cell (a cell with a value of 0).
2. **Try all possible numbers**: It tries all numbers from 1 to 9 in the empty cell.
3. **Check validity**: For each number, it checks if the number is valid in the current cell based on Sudoku rules (no duplicates in the same row, column, or 3x3 sub-grid).
4. **Recursive step**: If a valid number is found, it recursively attempts to fill in the rest of the board.
5. **Backtrack**: If it reaches a point where no valid numbers can be placed, it backtracks to the previous cell and tries the next number.
6. **Repeat**: This process repeats until the board is completely filled or no solution is found.

### AI Enhancements

The solver includes additional logic to make the solving process more efficient:

- **Constraint Propagation**: By applying constraints (like removing possibilities for a cell based on existing numbers in its row, column, and sub-grid), the algorithm reduces the number of potential candidates early on.
- **Heuristics**: The algorithm uses heuristics to decide the order in which cells are filled, such as selecting the cell with the fewest possibilities first (minimum remaining value heuristic).

