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
        self._solved = False  # T/F if sudoku puzzle has been solved
        self._started = False  # T/F if a game has started
        self._difficulty = "easy"  # easy, medium, hard, expert
        self._solution = None
        self._undo_stack = []
        self._redo_stack = []
        self._dict_prompt = {
            "menu": ("Sudoku Main Menu\nChoose from the following options:\n"
                     "1. Resume Game\n2. New Game\n3. Solve\n4. Verify Solution\n5. Exit\n", 5),
            "difficulty": ("Choose difficulty:\n1. Easy\n2. Medium\n3. Hard\n4. Expert\n", 4),
            "play": ("Choose from the following options:\n"
                     "1. Fill\n2. Unfill\n3. Undo\n4. Redo\n5. Reset\n6. Return to Main Menu\n", 6),
            "row": ("Row to be updated (1-9): ", n),
            "column": ("Column to be updated (1-9): ", n),
            "fill": ("Number to fill cell (1-9): ", n)
        }
        self._dict_diff = {
            "easy": (40, 45),
            "medium": (50, 55),
            "hard": (60, 65),
            "expert": (68, 73)
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

    def get_difficulty(self):
        """Returns current difficulty"""
        return self._difficulty

    def get_started(self):
        """Returns T/F whether game has started"""
        return self._started

    def get_immutable_grid(self):
        """Returns the immutable Sudoku grid"""
        return self._immutable_grid

    def get_dict_prompt(self):
        """Returns the dictionary of prompts"""
        return self._dict_prompt

    def get_dict_diff(self):
        """Returns the dictionary of difficulties"""
        return self._dict_diff

    def start_sudoku(self):
        """Starts the game"""
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
        if not self.get_started():
            return
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
        if not self.get_started():
            return print("No sudoku puzzle; start a new game!\n")

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
        """Sets the value of N for an NxN grid"""
        self._n = n

    def set_row(self, row):
        """Sets the number of rows"""
        self._row = row

    def set_col(self, col):
        """Sets the number of columns"""
        self._col = col

    def set_solved(self, value):
        """Sets True if sudoku game is solved, otherwise False"""
        self._solved = value

    def set_difficulty(self, user_input):
        """Sets difficulty of sudoku"""
        if user_input == 2:
            self._difficulty = "medium"
        elif user_input == 3:
            self._difficulty = "hard"
        elif user_input == 4:
            self._difficulty = "expert"
        else:
            self._difficulty = "easy"

    def set_started(self, value):
        """Sets True if sudoku game has started, otherwise False"""
        self._started = value

    def set_grid(self, row, col, num):
        """Sets the integer value in the grid at the specified cell"""
        self._grid[row][col] = num

    def set_immutable_grid(self, row, col, immutable):
        """Sets True if cell is immutable, otherwise False"""
        self._immutable_grid[row][col] = immutable

    def generate_sudoku(self):
        """Generates a random solvable sudoku board"""
        self.set_started(True)
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

        # removes random number of filled cells based on difficulty
        min_range, max_range = self.get_dict_diff()[str(self.get_difficulty())]
        total_removed = random.randint(min_range, max_range)
        cells_removed = 0
        while cells_removed < total_removed:
            cell = random.randint(0, N ** 2 - 1)
            x = cell // N
            y = cell % N

            if self.get_grid()[x][y] == 0:
                continue
            else:
                self.get_grid()[x][y] = 0
                cells_removed += 1

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
        if user_input == 1 or user_input == 2:
            if not self.get_started() or user_input == 2:
                self.set_difficulty(self.prompt(self.get_dict_prompt()["difficulty"]))
                self.clear_grid()
                self.init_sudoku(self.generate_sudoku())
            self.print_sudoku()
            self.play_sudoku(user_input)
        elif user_input == 3:
            self.reset_sudoku()
            self.solve_sudoku()
        elif user_input == 4:
            self.verify_sudoku()
        self.print_sudoku()
        return self.prompt(self.get_dict_prompt()["menu"])

    def play_sudoku(self, user_input):
        """Plays the sudoku game"""
        while user_input != 6:
            user_input = self.prompt(self.get_dict_prompt()["play"])
            if user_input == 1 or user_input == 2:
                ui_row = self.prompt(self.get_dict_prompt()["row"])
                ui_col = self.prompt(self.get_dict_prompt()["column"])
                if user_input == 1:
                    self._undo_stack.append((ui_row, ui_col, self.get_grid()[ui_row-1][ui_col-1]))
                    self.update_cell(ui_row, ui_col, self.prompt(self.get_dict_prompt()["fill"]))
                elif user_input == 2:
                    self._undo_stack.append((ui_row, ui_col, self.get_grid()[ui_row-1][ui_col-1]))
                    self.update_cell(ui_row, ui_col, 0)
                if self.get_immutable_grid()[ui_row][ui_col]:
                    self._undo_stack.pop()
            elif user_input == 3:
                if not self._undo_stack:
                    print("No moves to undo")
                else:
                    ui_row, ui_col, ui_num = self._undo_stack.pop()
                    self._redo_stack.append((ui_row, ui_col, self.get_grid()[ui_row-1][ui_col-1]))
                    self.update_cell(ui_row, ui_col, ui_num)
            elif user_input == 4:
                if not self._redo_stack:
                    print("No moves to redo")
                else:
                    ui_row, ui_col, ui_num = self._redo_stack.pop()
                    self._undo_stack.append((ui_row, ui_col, self.get_grid()[ui_row-1][ui_col-1]))
                    self.update_cell(ui_row, ui_col, ui_num)
            elif user_input == 5:
                self.reset_sudoku()
            self.print_sudoku() if user_input != 6 else None

    def reset_sudoku(self):
        """Resets sudoku board"""
        N = self.get_n()
        self._undo_stack, self._redo_stack = [], []
        for i in range(N):
            for j in range(N):
                if not self.get_immutable_grid()[i][j]:
                    self.set_grid(i, j, 0)
        self.set_solved(False)

    def clear_grid(self):
        """Clears sudoku board"""
        N = self.get_n()
        self._undo_stack, self._redo_stack = [], []
        for i in range(N):
            for j in range(N):
                self.set_grid(i, j, 0)
        self.set_solved(False)


if __name__ == "__main__":
    sudoku = Sudoku()
    # sudoku = Sudoku(12, 12, 12, (3, 4))
    sudoku.start_sudoku()
