# Based on the Sudoku Generator Algorithm (www.101computing.net/sudoku-generator-algorithm/)
from random import randint, shuffle
import json
import copy


def checkGrid(grid):
	""" A function to check if the grid is full """
	for row in range(0, 9):
		for col in range(0, 9):
			if grid[row][col] == 0:
				return False

	# We have a complete grid!
	return True


def solveGrid(grid):
	""" A backtracking/recursive function to check all possible combinations of numbers until a solution is found """
	global counter
	# Find next empty cell
	for i in range(0, 81):
		row = i//9
		col = i % 9
		if grid[row][col] == 0:
			for value in range(1, 10):
				# Check that this value has not already be used on this row
				if not(value in grid[row]):
					# Check that this value has not already be used on this column
					if not value in (grid[0][col], grid[1][col], grid[2][col], grid[3][col], grid[4][col], grid[5][col], grid[6][col], grid[7][col], grid[8][col]):
						# Identify which of the 9 squares we are working on
						square = []
						if row < 3:
							if col < 3:
								square = [grid[i][0:3]
									for i in range(0, 3)]
							elif col < 6:
								square = [grid[i][3:6]
									for i in range(0, 3)]
							else:
								square = [grid[i][6:9]
									for i in range(0, 3)]
						elif row < 6:
							if col < 3:
								square = [grid[i][0:3]
									for i in range(3, 6)]
							elif col < 6:
								square = [grid[i][3:6]
									for i in range(3, 6)]
							else:
								square = [grid[i][6:9]
									for i in range(3, 6)]
						else:
							if col < 3:
								square = [grid[i][0:3]
									for i in range(6, 9)]
							elif col < 6:
								square = [grid[i][3:6]
									for i in range(6, 9)]
							else:
								square = [grid[i][6:9]
									for i in range(6, 9)]
						# Check that this value has not already be used on this 3x3 square
						if not value in (square[0] + square[1] + square[2]):
							grid[row][col] = value
							if checkGrid(grid):
								counter += 1
								break
							else:
								if solveGrid(grid):
									return True
			break
	grid[row][col] = 0


def fillGrid(grid):
	""" A backtracking/recursive function to check all possible combinations of numbers until a solution is found """
	global counter
	numberList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	# Find next empty cell
	for i in range(0, 81):
		row = i//9
		col = i % 9
		if grid[row][col] == 0:
			shuffle(numberList)
			for value in numberList:
				# Check that this value has not already be used on this row
				if not(value in grid[row]):
					# Check that this value has not already be used on this column
					if not value in (grid[0][col], grid[1][col], grid[2][col], grid[3][col], grid[4][col], grid[5][col], grid[6][col], grid[7][col], grid[8][col]):
						# Identify which of the 9 squares we are working on
						square = []
						if row < 3:
							if col < 3:
								square = [grid[i][0:3]
									for i in range(0, 3)]
							elif col < 6:
								square = [grid[i][3:6]
									for i in range(0, 3)]
							else:
								square = [grid[i][6:9]
									for i in range(0, 3)]
						elif row < 6:
							if col < 3:
								square = [grid[i][0:3]
									for i in range(3, 6)]
							elif col < 6:
								square = [grid[i][3:6]
									for i in range(3, 6)]
							else:
								square = [grid[i][6:9]
									for i in range(3, 6)]
						else:
							if col < 3:
								square = [grid[i][0:3]
									for i in range(6, 9)]
							elif col < 6:
								square = [grid[i][3:6]
									for i in range(6, 9)]
							else:
								square = [grid[i][6:9]
									for i in range(6, 9)]
						# Check that this value has not already be used on this 3x3 square
						if not value in (square[0] + square[1] + square[2]):
							grid[row][col] = value
							if checkGrid(grid):
								return True
							else:
								if fillGrid(grid):
									return True
			break
	grid[row][col] = 0


data = {}
# A higher number of attempts will end up removing more numbers from the grid
# Potentially resulting in more difficiult grids to solve!
for attempts, level in [(25, "easy"), (40, "medium"), (70, "hard")]:
	print(f"Generating level '{level}'")
	# Initialize empty grid
	grid = [[0]*9 for _ in range(9)]

	# Generate a fully solved grid
	fillGrid(grid)

	# Save grid to output later
	solved_grid = copy.deepcopy(grid)

	# Start removing numbers one by one
	counter = 1
	while attempts > 0:
		# Select a random cell that is not already empty
		row = randint(0, 8)
		col = randint(0, 8)
		while grid[row][col] == 0:
			row = randint(0, 8)
			col = randint(0, 8)
		# Remember its cell value in case we need to put it back
		backup = grid[row][col]
		grid[row][col] = 0

		# Take a full copy of the grid
		copy_grid = copy.deepcopy(grid)

		# Count the number of solutions that this grid has (using a backtracking approach implemented in the solveGrid() function)
		counter = 0
		solveGrid(copy_grid)
		# If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
		if counter != 1:
			grid[row][col] = backup

		# We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
		attempts -= 1

	data[level] = {
		"solved": copy.deepcopy(solved_grid),
		"start": copy.deepcopy(grid)
	}

with open("sudoko.json", "w") as f:
	json.dump(data, f)

print("Finished")
