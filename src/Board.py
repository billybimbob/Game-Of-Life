from random import randint
import argparse

class Board:
    def __init__(self, width, height, *, gen_start=None, check_alive=None, find_neighbors=None):
        def default_start(): #don't do anything with params
            return [[randint(0, 1) for _ in range(width)] for _ in range(height)]
        
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

        if gen_start is None:      gen_start = default_start
        if check_alive is None:    check_alive = default_check
        if find_neighbors is None: find_neighbors = default_neighbors

        self.width = width
        self.height = height
        self.data = gen_start() #could potentially not be 0 or 1
        self.check_alive = check_alive
        self.find_neighbors = find_neighbors


    def update(self): #updates for one cycle
        def new_alive(row, col):
            return self.check_alive(
                self.data[row][col],
                self.find_neighbors(self.data, self.width, self.height, row, col)
            )

        self.data = [ [new_alive(row,col) for col in range(self.width)] for row in range(self.height) ]

    def __str__(self):
        accum = []
        for row in range(self.height):
            accum.append('|')
            for col in range(self.width):
                char = ' ' if self.data[row][col]==0 else '#'
                accum.append(char)
            accum.append('|\n')

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
    def __init__(self, *, width=10, height=10, start_state=None, neighbors=None):
        if start_state is not None: #assume 2d grid
            def get_start():
                return start_state
            width = len(start_state[0])
            height = len(start_state)
            self.board = Board(width, height, gen_start=get_start, find_neighbors=neighbors)
        else:
            self.board = Board(width, height, find_neighbors=neighbors) #add later

    @staticmethod
    def read_start(file_name):
        with open(file_name, 'r') as reading:
            values = [ [int(char) for char in line if char=='0' or char=='1'] for line in reading ]
            return values

    def loop(self, loops=0):
        count = 0
        while loops==0 or count<=loops:
            print(self.board)
            self.board.update()
            count += 1


if __name__ == "__main__":
    def zero_board(width, height):
        return [ [0]*width for _ in range(height)]
    def alive_board(width, height):
        return [ [1]*width for _ in range(height)]

    def parse_arguements():
        parser = argparse.ArgumentParser()
        parser.add_argument("--file", "-f",   help="file to set the start state")
        parser.add_argument("--cycles", "-c", help="number of cycles for the board")

        return parser.parse_args()

    def no_wrap_neighbors(data, width, height, row, col):
        def in_bounds(m_row, m_col):
            return m_row >= 0 and m_row < height \
                and m_col >= 0 and m_col < width

        mods = [-1, 0, 1]
        checking = [data[row+r][col+c] for r in mods for c in mods if (r!=0 or c!=0) and in_bounds(row+r, col+c)]
        return sum(checking)

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

    args = parse_arguements()
    start = Game.read_start(args.file) if args.file else init_state2

    test = Game(start_state=start)
    test.loop(4)