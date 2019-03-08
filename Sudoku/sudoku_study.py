# reference: https://hackernoon.com/sudoku-and-backtracking-6613d33229af

# Sudoku & Backtracking
#
# Problem
# Given a, possibly, partially filled grid of size ‘n’, completely fill the grid with number between 1 and ‘n’.
#
# Goal
# Goal is defined for verifying the solution. Once the goal is reached, searching terminates. A fully filled grid is a solution if:
#
# 1. Each row has all numbers form 1 to ‘n’.
# 2. Each column has all numbers form 1 to ‘n’.
# 3. Each sub-grid (if any) has all numbers form 1 to ‘n’.
#
# Constraints
# Constraints are defined for verifying each candidate. A candidate is valid if:
#
# 1. Each row has unique numbers form 1 to ’n’ or empty spaces.
# 2. Each column has unique numbers form 1 to ‘n’ or empty spaces.
# 3. Each sub-grid (if any) has unique numbers form 1 to ‘n’ or empty spaces.
#
# Termination conditions
# Typically, backtracking algorithms have termination conditions other than reaching goal. These help with failures in solving the problem and special cases of the problem itself.
#
# 1. There are no empty spots left to fill and the candidate still doesn’t qualify as a the solution.
# 2. There are no empty spots to begin with, i.e., the grid is already fully filled.
#
# Step-by-step algorithm
# Here’s how our code will “guess” at each step, all the way to the final solution:
#
# 1. Make a list of all the empty spots.
# 2. Select a spot and place a number, between 1 and ‘n’, in it and validate the candidate grid.
# 3. If any of the constraints fails, abandon candidate and repeat step 2 with the next number. Otherwise, check if the goal is reached.
# 4. If a solution is found, stop searching. Otherwise, repeat steps 2 to 4.


#!/usr/bin/python3

grid3 = [
  [2, 0, 3],
  [1, 0, 0],
  [0, 0, 1],
]

grid4 = [
  [4, 0, 0, 0],
  [0, 2, 0, 4],
  [2, 0, 3, 0],
  [0, 0, 0, 2],
]

grid9 = [
  [0, 0, 0, 0, 0, 0, 6, 8, 0],
  [0, 0, 0, 0, 7, 3, 0, 0, 9],
  [3, 0, 9, 0, 0, 0, 0, 4, 5],
  [4, 9, 0, 0, 0, 0, 0, 0, 0],
  [8, 0, 3, 0, 5, 0, 9, 0, 2],
  [0, 0, 0, 0, 0, 0, 0, 3, 6],
  [9, 6, 0, 0, 0, 0, 3, 0, 8],
  [7, 0, 0, 6, 8, 0, 0, 0, 0],
  [0, 2, 8, 0, 0, 0, 0, 0, 0],
]

solution = None  # solution grid


def print_grid(grid):
  '''pretty print Sudoku grid'''
  for row in grid:
    print(' '.join([str(x) for x in row if x != 0]))


def copy_grid(grid):
  return [row[:] for row in grid]


def check_rows(grid):
  '''check rows for constraint validity'''
  for row in grid:
    xs = set()

    for x in row:
      if x == 0:
        continue

      if x in xs:
        return False

      xs.add(x)

  return True


def check_cols(grid):
  '''check columns for constraint validity'''
  cols = [[row[i] for row in grid] for i in range(n)]

  return check_rows(cols)


def check_sub_grids(grid):
  '''check sub-grids for constraint validity'''
  m = int(n ** 0.5)

  # sub-grids exist for squared grids only
  if m*m != n:
    return True

  for i in range(m):
    for j in range(m):
      sub_grid = [row[j*m:(j+1)*m] for row in grid[i*m:(i+1)*m]]
      xs = set()

      for row in sub_grid:
        for x in row:
          if x == 0:
            continue

          if x in xs:
            return False

          xs.add(x)

  return True


def check_solution(grid):
  '''check solution grid for goal validity'''
  return sum([row.count(0) for row in grid]) == 0


def solve(grid, spots, x):
  global solution

  # all spots filled: stop searching
  if len(spots) == 0:
    return

  # another search solved the grid: stop searching
  if solution != None:
    return

  # set the (i, j) cell to x
  (i, j) = spots[0]
  grid[i][j] = x

  # the grid is invalid: stop searching
  is_grid_valid = check_rows(grid) and check_cols(grid) and check_sub_grids(grid)
  if is_grid_valid == False:
    return

  # the grid is valid and solved: stop searching
  is_grid_solved = check_solution(grid)
  if is_grid_solved == True:
    solution = grid
    return

  # here, the grid is valid but not solved: continue searching
  for x in range(n):
    spots1 = spots[1:]  # clone `spots` array starting from 1st index
    solve(copy_grid(grid), spots1, x+1)


def main():
  # list all spots
  spots = []
  for i in range(n):
    for j in range(n):
      if grid[i][j] == 0:
        spots.append((i, j))

  # solve grid
  for x in range(n):
    solve(copy_grid(grid), spots, x+1)

  print_grid(solution)


if __name__ == '__main__':
  grid = grid9
  n = len(grid)
  main()
