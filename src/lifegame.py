from random import randint
from typing import List, Callable
import argparse

class Board:
    def __init__(self, width, height, *, start=None, check_alive=None, find_neighbors=None):

        def default_check(spot, neighbors):
            if spot == 1:
                return 1 if neighbors==2 or neighbors==3 else 0
            else:
                return 1 if neighbors==3 else 0

        def default_neighbors(data, width, height, row, col): #for param functs
            def norm_idx(idx, row=True): # allows for wraparound
                if idx < 0 and row:
                    return idx + height
                elif idx < 0 and not row:
                    return idx + width
                elif idx >= height and row:
                    return idx % height
                elif idx >= width and not row:
                    return idx % width
                else:
                    return idx

            def neighbor_val(p_row, p_col):
                return data[norm_idx(p_row)][norm_idx(p_col, False)]

            mods = [-1, 0, 1] #assume square grid
            look = [ neighbor_val(row+rmod, col+cmod) for rmod in mods for cmod in mods \
                if rmod!=0 or cmod!=0 ] #exclude spot
            return sum(look) #assume 1 or 0 val, could change

        def check_start(board: List[list]): #easier check, and creates copy
            max_width = 0
            board_copy = []
            for row in board:
                if len(row) > max_width: max_width = len(row)
                #default unknown values to 0
                board_copy.append([val if val==0 or val==1 else 0 for val in row])

            for row in board_copy: #make all width the same
                diff = max_width - len(row) #should never be 0
                row.extend([0]*diff)

            return board_copy

        if check_alive is None:    check_alive = default_check
        if find_neighbors is None: find_neighbors = default_neighbors
        if start is None:
            start = [[randint(0, 1) for _ in range(width)] for _ in range(height)]

        self.data = check_start(start)
        self.width = len(self.data[0]) #dim based on normed start
        self.height = len(self.data)

        self.check_alive = check_alive
        self.find_neighbors = find_neighbors


    def update(self): #updates for one cycle
        def new_alive(row, col):
            return self.check_alive (
                self.data[row][col],
                self.find_neighbors(self.data, self.width, self.height, row, col)
            )

        self.data = [ [new_alive(row,col) for col in range(self.width)] for row in range(self.height) ]

    def __str__(self):
        edges = ['|'] + ['-']*self.width + ['|\n']

        accum: List[str] = []
        accum.extend(edges)
        for row in range(self.height):
            accum.append('|')
            for col in range(self.width):
                char = ' ' if self.data[row][col]==0 else '#'
                accum.append(char)
            accum.append('|\n')
        accum.extend(edges)

        return ''.join(accum)

    def __eq__(self, other):
        def iter_check():
            accum = True
            for a, b in zip(self, other):
                accum = accum and (a==b)
                if not accum: break
            return accum

        return self.height==other.height \
            and self.width==other.width \
            and iter_check()

    def __iter__(self):
        yield from (self.data[i][j] for i in range(self.height) for j in range(self.width))



class Game:
    def __init__(self, *, width=10, height=10,
        start_state: List[list] = None,
        alive: Callable[[int, int], int] = None,
        neighbors: Callable[[int, int, int, int, int], int] = None,
        render: Callable[[str], None] = None):

        def default_render(board_info):
            print(board_info)

        if render is None: render = default_render
        self.render = render
        self.board = Board(width, height, start=start_state, find_neighbors=neighbors)

    @staticmethod
    def read_start(file_name):
        with open(file_name, 'r') as reading:
            values = [ [int(char) for char in line if char=='0' or char=='1'] for line in reading ]
            return values

    @staticmethod
    def parse_arguements():
        parser = argparse.ArgumentParser()
        parser.add_argument("--file", "-f",   help="file to set the start state")
        parser.add_argument("--cycles", "-c", help="number of cycles for the board")

        return parser.parse_args()

    def run(self, limit=1):
        count = 0
        while count<limit:
            self.render(str(self.board))
            self.board.update()
            count += 1



def zero_board(width, height):
    return [ [0]*width for _ in range(height)]

def alive_board(width, height):
    return [ [1]*width for _ in range(height)]

def no_wrap_neighbors(data, width, height, row, col):
    def in_bounds(m_row, m_col):
        return m_row >= 0 and m_row < height \
            and m_col >= 0 and m_col < width

    mods = [-1, 0, 1]
    checking = [data[row+r][col+c] for r in mods for c in mods if (r!=0 or c!=0) and in_bounds(row+r, col+c)]
    return sum(checking)


if __name__ == "__main__":

    # test = Game(start_state=alive_board(3, 5))
    init_state1 = [
        [0,0,1],
        [0,1,1],
        [0,0,0]
    ]
    init_state2 = [
        [0,0,0,0],
        [0,0,1,0],
        [0,1,1,0],
        [0,0,0,0]
    ]
    #test = Game(start_state=init_state1, neighbors=no_wrap_neighbors)

    args = Game.parse_arguements()
    start = Game.read_start(args.file) if args.file else init_state2

    test = Game(start_state=start)
    test.run(4)
