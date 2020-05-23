import timeit
from collections import deque

class SudokuBoard:
    def __init__(self, grid):
        assert len(grid) == 9 and len(grid[0]) == 9, "wrong size"
        self.grid = grid
        
    def __str__(self):
        s = ""
        for i, row in enumerate(self.grid):
            s += "  {} {} {}   {} {} {}   {} {} {}  \n".format(*row)
            if i in (2, 5):
                s += f"{' ':25}\n"
        return s.rstrip('\n')
        
    def get_block(self, block_row, block_col):
        x = block_row * 3
        y = block_col * 3
        return [self.grid[x][y],  self.grid[x][y+1],   self.grid[x][y+2],
                self.grid[x+1][y], self.grid[x+1][y+1], self.grid[x+1][y+2],
                self.grid[x+2][y], self.grid[x+2][y+1], self.grid[x+2][y+2]]

    def get_row(self, row):
        return self.grid[row]

    def get_col(self, col):
        return [row[col] for row in self.grid]

    def is_solved(self):
        return not any(0 in row for row in self.grid)
        # faster?
        # numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        # for row in self.grid:
        #    if set(row) != numbers:
        #        return False
        # for col in range(9):
        #    if set(self.get_col(col)) != numbers:
        #        return False
        # for i in range(3):
        #    for j in range(3):
        #        if set(self.get_block(i, j)) != numbers:
        #            return False
        # return True

    def get_possible_values(self, row, col):
        values = set(self.get_block(row // 3, col // 3) + self.get_row(row) + self.get_col(col))
        return values.symmetric_difference(range(10))

    def get_empty_square(self):
        for x, row in enumerate(self.grid):
            for y, val in enumerate(row):
                if val == 0:
                    return x, y

    def solve(self):
        stack = deque([Node(self)])

        while len(stack) > 0:
            parent_node = stack.pop()
            row, col = parent_node.board.get_empty_square()
            
            for value in parent_node.board.get_possible_values(row, col):
                new_board_grid = list(map(list, parent_node.board.grid))
                new_board_grid[row][col] = value

                node = Node(SudokuBoard(new_board_grid), parent_node.depth + 1)

                if node.board.is_solved():
                    self.solution = node.board
                    return

                stack.append(node)

        # No solution found
        self.solution = None
    
class Node:
    def __init__(self, board: SudokuBoard, depth = 0):
        self.board = board
        self.depth = depth

def read_file(path: str, sudoku_boards: list):
    file = open(path, 'r')
    lines = file.readlines()

    for line_num, line in enumerate(lines):
        if "SUDOKU" in line:
            board = []
            for line in lines[line_num + 1 : line_num + 10]:
                board.append([int(i) for i in line if i.isdigit()])
            sudoku_boards.append(SudokuBoard(board))
        if "EOF" in line:
            break

    file.close()

def print_board(board, i):
    length = str(board).find("\n")
    print(f"⌜{f'Board {i}':^{length - 2}}⌝")
    print(board.solution or f"{'(No solution found)':^{length}}")
    print(f"⌞{' ':{length - 2}}⌟\n")

def main():
    sudoku_boards = []
    read_file("sudoku", sudoku_boards)

    start_time = timeit.default_timer()
    for board in sudoku_boards:
        board.solve()
    print(f"Execution time: {timeit.default_timer() - start_time}\n")

    # Print solutions
    for i, board in enumerate(sudoku_boards, start = 1):
        print_board(board, i)

if __name__ == '__main__':
    main()