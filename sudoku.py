# A sudoku solving and verifying algorithm

import random
import math

N = 9


def generate_sudoku():
    """"""
    grid = [[0 for y in range(N)] for x in range(N)]
    playable_num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    num_sets = (playable_num, list(playable_num), list(playable_num))
    sqrt_N = int(math.sqrt(N))

    for i in range(0, N, sqrt_N):
        for j in range(sqrt_N):
            for k in range(sqrt_N):
                grid[i + j][i + k] = num_sets[i // 3].pop(random.randrange(len(num_sets[i // 3])))

    solve_sudoku(grid)
    # print_sudoku(grid)

    total_rm = random.randint(36, 72)
    for i in range(total_rm):
        cell = random.randint(0, 80)
        x = cell // N
        y = cell % N

        if grid[x][y] == 0:
            i -= 1
        else:
            grid[x][y] = 0

    return grid


def init_sudoku(grid):
    """"""
    immutable_cell = [[0 for y in range(N)] for x in range(N)]
    for i in range(N):
        for j in range(N):
            if grid[i][j] != 0:
                immutable_cell[i][j] = True
            else:
                immutable_cell[i][j] = False
    return immutable_cell


def update_cell(init_grid, grid, row, col, num):
    """"""
    if row < 1 or row > 9 or col < 1 or col > 9:
        print("Invalid: Chosen cell outside of grid")
        return
    if not init_grid[row-1][col-1]:
        grid[row-1][col-1] = num
    else:
        print("Initialized sudoku cell can not be updated")


def prompt(prompt, num_options):
    """"""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("ValueError: Response must be a number\n")
            continue

        if 0 < value <= num_options:
            break
        else:
            print("Invalid: Response must be a valid number\n")
            continue
    return value


def check_row(grid, row, col, num):
    """Checks the row"""
    for i in range(N):
        if i == col:
            continue
        if grid[row][i] == num:
            return False
    return True


def check_col(grid, row, col, num):
    """Checks the column"""
    for i in range(N):
        if i == row:
            continue
        if grid[i][col] == num:
            return False
    return True


def check_3x3(grid, row, col, num):
    """Checks the 3x3 square"""
    top_left_row, top_left_col = 3 * (row // 3), 3 * (col // 3)
    for x in range(top_left_row, top_left_row + 3):
        for y in range(top_left_col, top_left_col + 3):
            if x == row and y == col:
                continue
            if grid[x][y] == num:
                return False
    return True


def valid_num_in_cell(grid, row, col, num):
    """Determines whether the number is valid in the cell. If valid, returns True, otherwise False."""
    return check_row(grid, row, col, num) and check_col(grid, row, col, num) and check_3x3(grid, row, col, num)


def next_cell(grid, row=0, col=0):
    """Finds the next empty cell"""
    for i in range(row, N):
        for j in range(col, N):
            if grid[i][j] == 0:
                return i, j
        col = 0
    return -1, -1


def solve_sudoku(grid, row=0, col=0):
    """Solves sudoku using backtracking method"""
    i, j = next_cell(grid, row, col)
    if i == -1:
        return True
    for k in range(1, N + 1):
        if valid_num_in_cell(grid, i, j, k):
            grid[i][j] = k
            if solve_sudoku(grid, i, j):
                return True
            grid[i][j] = 0
    return False


def verify_sudoku(grid):
    """Verifies the solution of the sudoku puzzle"""
    for i in range(N):
        for j in range(N):
            num = grid[i][j]
            if not check_row(grid, i, j, num) or not check_col(grid, i, j, num) or not check_3x3(grid, i, j, num):
                return "Not Solved, Try Again!"
    return "Solved!"


def print_sudoku(grid):
    """Prints sudoku grid"""
    len_row = len(grid)
    if len_row < 1:
        return
    elif len_row >= 1:
        len_col = len(grid[0])
        if len_col < 1:
            return

    for i in range(len_row):
        for j in range(len_col):
            cell = grid[i][j]
            if i == 0 and j == 0:
                print("    C  1  2  3     4  5  6     7  8  9")
                print("       -  -  -     -  -  -     -  -  -\nR")

            if j == 0:
                print(str(i+1) + '|     ', end="")
            if cell == 0:
                print('.', end=" ")
            else:
                print(cell, end=" ")
            if (j + 1) % 3 == 0 and j < N - 1:
                print(' |', end=" ")

            if j != N - 1:
                print(' ', end="")
        print()
        if (i + 1) % 3 == 0 and i < N - 1:
            print("       -  -  -  +  -  -  -  +  -  -  -")
    print()


def chosen_option(ui, grid, init_grid):
    if ui == 1:
        print_sudoku(grid)
        play = prompt("Choose from the following options:\n1. Fill\n2. Unfill\n3. Return to Main Menu\n", 3)

        while play != 3:
            if play == 1:
                ui_row = prompt("Row to be updated (1-9): ", N)
                ui_col = prompt("Column to be updated (1-9): ", N)
                ui_num = prompt("Number to fill cell (1-9): ", N)
                update_cell(init_grid, grid, ui_row, ui_col, ui_num)
                print_sudoku(grid)
            elif play == 2:
                ui_row = prompt("Row to be updated (1-9): ", N)
                ui_col = prompt("Column to be updated (1-9): ", N)
                update_cell(init_grid, grid, ui_row, ui_col, 0)
                print_sudoku(grid)
            play = prompt("Choose from the following options:\n1. Fill\n2. Unfill\n3. Return to Main Menu\n", 3)

            if play == 3:
                ui = prompt("Main Menu\nChoose from the following options:\n1. Play\n2. Solve\n3. Verify Solution\n4. Exit\n", 4)
                return ui
        return 1
    elif ui == 2:
        reset_sudoku(grid, init_grid)
        solve_sudoku(grid)
        print_sudoku(grid)
        ui = prompt("Main Menu\nChoose from the following options:\n1. Play\n2. Solve\n3. Verify Solution\n4. Exit\n", 4)
        return ui
    elif ui == 3:
        print_sudoku(grid)
        print(verify_sudoku(grid))
        ui = prompt("Main Menu\nChoose from the following options:\n1. Play\n2. Solve\n3. Verify Solution\n4. Exit\n", 4)
        return ui


def reset_sudoku(grid, init_grid):
    for i in range(N):
        for j in range(N):
            if not init_grid[i][j]:
                grid[i][j] = 0

# BASIC TESTING
if __name__ == "__main__":
    sudoku = generate_sudoku()
    immutable = init_sudoku(sudoku)
    print_sudoku(sudoku)
    ui = prompt("Main Menu\nChoose from the following options:\n1. Play\n2. Solve\n3. Verify Solution\n4. Exit\n", 4)
    # ui = input("Choose from the following options (Type the number chosen):\n1. Play\n2. Solve\n3. Verify Solution\n")
    while ui != 4:
        ui = chosen_option(ui, sudoku, immutable)

    # print(solve_sudoku(sudoku))
    # print_sudoku(sudoku)
    # print(verify_sudoku(sudoku))
    # hardest_sudoku = [
    #     [8, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 3, 6, 0, 0, 0, 0, 0],
    #     [0, 7, 0, 0, 9, 0, 2, 0, 0],
    #     [0, 5, 0, 0, 0, 7, 0, 0, 0],
    #     [0, 0, 0, 0, 4, 5, 7, 0, 0],
    #     [0, 0, 0, 1, 0, 0, 0, 3, 0],
    #     [0, 0, 1, 0, 0, 0, 0, 6, 8],
    #     [0, 0, 8, 5, 0, 0, 0, 1, 0],
    #     [0, 9, 0, 0, 0, 0, 4, 0, 0]]
    # print_sudoku(hardest_sudoku)
    # print(solve_sudoku(hardest_sudoku))
    # print_sudoku(hardest_sudoku)
    # print(verify_sudoku(hardest_sudoku))
