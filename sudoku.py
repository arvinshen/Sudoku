# A sudoku solving and verifying algorithm

N = 9

def check_row(grid, row, num):
    pass

def check_col(grid, col, num):
    pass

def check_3x3(grid, row, col, num):
    pass

def valid_num_in_cell(grid, row, col, num):
    return check_row(grid, row, num) and check_col(grid, col, num) and check_3x3(grid, row, col, num)

def next_cell(grid, row=0, col=0):
    for i in range(row, N):
        for j in range(col, N):
            if grid[row][col] == 0:
                return i, j
    return -1, -1

def solve_sudoku(grid, row=0, col=0):
    """Solves sudoku using backtracking method"""
    i, j = next_cell(grid, row, col)
    if i == -1:
        return True
    for k in range(1, N+1):
        if valid_num_in_cell(grid, i, j, k):
            grid[i][j] = k
            if solve_sudoku(grid, i, j):
                return True
            grid[i][j] = 0
    return False


def verify_sudoku(grid):
    """Verifies the solution of the sudoku puzzle"""


    return True


def print_sudoku(grid):
    if not grid:
        return
    for i in range(N):
        for j in range(N):
            cell = grid[i][j]
            if cell == 0:
                print('.', end=" ")
            else:
                print(cell, end=" ")
            if (j + 1) % 3 == 0 and j < N-1:
                print(' |', end=" ")

            if j != N-1:
                print(' ', end="")
        print()
        if (i + 1) % 3 == 0 and i < N-1:
            print("-  -  -  +  -  -  -  +  -  -  -")


# BASIC TESTING
if __name__ == "__main__":
    hardest_sudoku = [
        [8,0,0,0,0,0,0,0,0],
        [0,0,3,6,0,0,0,0,0],
        [0,7,0,0,9,0,2,0,0],
        [0,5,0,0,0,7,0,0,0],
        [0,0,0,0,4,5,7,0,0],
        [0,0,0,1,0,0,0,3,0],
        [0,0,1,0,0,0,0,6,8],
        [0,0,8,5,0,0,0,1,0],
        [0,9,0,0,0,0,4,0,0]]
    print_sudoku(hardest_sudoku)