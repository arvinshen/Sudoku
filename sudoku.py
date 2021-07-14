# A playable sudoku game with solving and verifying algorithms

import random
import math


class Sudoku:
    """Represents a classic Sudoku game"""

    def __init__(self, n=9, row=9, col=9, block_dim=(3, 3)):
        """Initializes Sudoku object"""
        self._n = n
        self._row = row
        self._col = col
        self._block_dim = block_dim
        self._grid = [[0 for y in range(n)] for x in range(n)]
        self._immutable_grid = [[False for y in range(n)] for x in range(n)]
        self._playable_num = ()
        self._solved = False
        self._solution = None
        self._dict_prompt = {
            "menu": ("Sudoku Main Menu\nChoose from the following options:\n"
                     "1. Play\n2. Solve\n3. Verify Solution\n4. Reset\n5. Exit\n", 5),
            "difficulty": ("Choose difficulty:\n1. Easy\n2. Medium\n3. Hard", 3),
            "play": ("Choose from the following options:\n1. Fill\n2. Unfill\n3. Return to Main Menu\n", 3),
            "row": ("Row to be updated (1-9): ", n),
            "column": ("Column to be updated (1-9): ", n),
            "fill": ("Number to fill cell (1-9): ", n)
        }
        for i in range(n):
            self._playable_num = self._playable_num + (i + 1,)

    # Queries
    def get_n(self):
        """Returns the value of N"""
        return self._n

    def get_row(self):
        """Returns the number of rows"""
        return self._row

    def get_col(self):
        """Returns the number of columns"""
        return self._col

    def get_block_dim(self):
        """Returns the dimensions of one block"""
        return self._block_dim

    def get_grid(self):
        """Returns the Sudoku grid"""
        return self._grid

    def get_playable_num(self):
        """Returns the tuple of playable numbers"""
        return self._playable_num

    def get_solved(self):
        """Returns T/F whether Sudoku is solved"""
        return self._solved

    def get_immutable_grid(self):
        """Returns the immutable Sudoku grid"""
        return self._immutable_grid

    def get_dict_prompt(self):
        """Returns the dictionary of prompts"""
        return self._dict_prompt

    def start_sudoku(self):
        """Starts the game"""
        self.init_sudoku(self.generate_sudoku())
        self.print_sudoku()
        player_input = self.prompt(self.get_dict_prompt()["menu"])
        while player_input != 5:
            player_input = self.chosen_option(player_input)

    def prompt(self, prompt_tuple):
        """Prompts and validates user input"""
        while True:
            try:
                prompt = prompt_tuple[0]
                value = int(input(prompt))
            except ValueError:
                print("ValueError: Response must be a number\n")
                continue

            num_options = prompt_tuple[1]
            if 0 < value <= num_options:
                break
            else:
                print("Invalid: Response must be a valid number\n")
                continue
        return value

    def check_row(self, row, col, num):
        """Checks the row"""
        for i in range(self.get_n()):
            if i == col:
                continue
            if self.get_grid()[row][i] == num:
                return False
        return True

    def check_col(self, row, col, num):
        """Checks the column"""
        for i in range(self.get_n()):
            if i == row:
                continue
            if self.get_grid()[i][col] == num:
                return False
        return True

    def check_3x3(self, row, col, num):
        """Checks the 3x3 square"""
        block_row = self.get_block_dim()[0]
        block_col = self.get_block_dim()[1]
        top_left_row, top_left_col = block_row * (row // block_row), block_col * (col // block_col)
        for x in range(top_left_row, top_left_row + block_row):
            for y in range(top_left_col, top_left_col + block_col):
                if x == row and y == col:
                    continue
                if self.get_grid()[x][y] == num:
                    return False
        return True

    def valid_num_in_cell(self, row, col, num):
        """Determines whether the number is valid in the cell. If valid, returns True, otherwise False."""
        return self.check_row(row, col, num) and self.check_col(row, col, num) and self.check_3x3(row, col, num)

    def next_cell(self, row=0, col=0):
        """Finds the next empty cell"""
        for i in range(row, self.get_n()):
            for j in range(col, self.get_n()):
                if self.get_grid()[i][j] == 0:
                    return i, j
            col = 0
        return -1, -1

    def verify_sudoku(self):
        """Verifies the solution of the sudoku puzzle"""
        for i in range(self.get_n()):
            for j in range(self.get_n()):
                num = self.get_grid()[i][j]
                if self.get_grid()[i][j] == 0 or not self.check_row(i, j, num) \
                        or not self.check_col(i, j, num) or not self.check_3x3(i, j, num):
                    self.set_solved(False)
                    return print("Not Solved, Try Again!\n")
        self.set_solved(True)
        return print("Solved!\n")

    def print_sudoku(self):  # Update to output dependent on specified block dimensions (not just for 9x9 with 3x3 blocks
        # but also for 12x12 with 3x4 blocks, 16x16 with 4x4 blocks, etc).
        """Prints sudoku grid"""
        len_row = self.get_row()
        if len_row < 1:
            return
        elif len_row >= 1:
            len_col = self.get_col()
            if len_col < 1:
                return

        N = self.get_n()
        for i in range(len_row):
            for j in range(len_col):
                cell = self.get_grid()[i][j]
                if i == 0 and j == 0:
                    print("    C  1  2  3     4  5  6     7  8  9")
                    print("       -  -  -     -  -  -     -  -  -\nR")

                if j == 0:
                    print(str(i + 1) + '|     ', end="")
                if cell == 0:
                    print('.', end=" ")
                else:
                    print(cell, end=" ")
                if (j + 1) % self.get_block_dim()[1] == 0 and j < N - 1:
                    print(' |', end=" ")

                if j != N - 1:
                    print(' ', end="")
            print()
            if (i + 1) % self.get_block_dim()[0] == 0 and i < N - 1:
                print("       -  -  -  +  -  -  -  +  -  -  -")
        print()

    # Commands
    def set_n(self, n):
        self._n = n

    def set_row(self, row):
        self._row = row

    def set_col(self, col):
        self._col = col

    def set_solved(self, value):
        self._solved = value

    def set_grid(self, row, col, num):
        self._grid[row][col] = num

    def set_immutable_grid(self, row, col, immutable):
        self._immutable_grid[row][col] = immutable

    def generate_sudoku(self):
        """Generates a random solvable sudoku board"""
        N = self.get_n()
        num_sets = [list(self.get_playable_num()) for i in range(min(self.get_row(), self.get_col()))]
        sqrt_N = int(math.sqrt(N))

        # fills blocks diagonally from 1st block (upper left corner) to 2nd block (center) to 3rd block (bottom right corner)
        for i in range(0, N, sqrt_N):
            for j in range(sqrt_N):
                for k in range(sqrt_N):
                    self.set_grid(i + j, i + k, num_sets[i // self.get_block_dim()[1]].pop(
                        random.randrange(len(num_sets[i // self.get_block_dim()[1]]))))

        self.solve_sudoku()
        self._solution = [row[:] for row in self.get_grid()]

        # removes random number of filled cells
        total_removed = random.randint(36, 72)
        for i in range(total_removed):
            cell = random.randint(0, N ** 2 - 1)
            x = cell // N
            y = cell % N

            if self.get_grid()[x][y] == 0:
                i -= 1
            else:
                self.get_grid()[x][y] = 0

        return self.get_grid()

    def init_sudoku(self, grid):
        """An initialized sudoku board determining which cells are immutable (i.e. starting grid)"""
        for i in range(self.get_n()):
            for j in range(self.get_n()):
                if grid[i][j] != 0:
                    self.set_immutable_grid(i, j, True)
                else:
                    self.set_immutable_grid(i, j, False)
        return self.get_immutable_grid()

    def update_cell(self, row, col, num):
        """Updates the cell with the user's chosen number"""
        if row < 1 or row > self.get_row() or col < 1 or col > self.get_col():
            print("Invalid: Chosen cell outside of grid")
            return
        if not self.get_immutable_grid()[row - 1][col - 1]:
            self.set_grid(row - 1, col - 1, num)
        else:
            print("Initialized sudoku cell can not be updated")

    def solve_sudoku(self, row=0, col=0):
        """Solves sudoku using backtracking method"""
        if self.get_solved():
            return True
        i, j = self.next_cell(row, col)
        if i == -1:
            return True
        for k in range(1, self.get_n() + 1):
            if self.valid_num_in_cell(i, j, k):
                self.set_grid(i, j, k)
                if self.solve_sudoku(i, j):
                    return True
                self.set_grid(i, j, 0)
        return False

    def chosen_option(self, user_input):
        """Executes chosen option from main menu and play"""
        if user_input == 1:
            while user_input != 3:
                user_input = self.prompt(self.get_dict_prompt()["play"])
                if user_input == 1 or user_input == 2:
                    ui_row = self.prompt(self.get_dict_prompt()["row"])
                    ui_col = self.prompt(self.get_dict_prompt()["column"])
                    if user_input == 1:
                        ui_num = self.prompt(self.get_dict_prompt()["fill"])
                        self.update_cell(ui_row, ui_col, ui_num)
                    elif user_input == 2:
                        self.update_cell(ui_row, ui_col, 0)
                    self.print_sudoku()
        elif user_input == 2:
            self.reset_sudoku()
            self.solve_sudoku()
        elif user_input == 3:
            self.verify_sudoku()
        elif user_input == 4:
            self.reset_sudoku()
        self.print_sudoku()
        return self.prompt(self.get_dict_prompt()["menu"])

    def reset_sudoku(self):
        """Resets sudoku board"""
        N = self.get_n()
        for i in range(N):
            for j in range(N):
                if not self.get_immutable_grid()[i][j]:
                    self.set_grid(i, j, 0)
        self.set_solved(False)


if __name__ == "__main__":
    sudoku = Sudoku()
    # sudoku = Sudoku(12, 12, 12, (3, 4))
    sudoku.start_sudoku()
