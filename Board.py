from random import randint

class Board:

    def __init__(self, width, height, gen_start=None, check_alive=None, find_neighbors=None):
        def default_start(): #don't do anything with params
            return [[randint(0, 1) for _ in range(width)] for _ in range(height)]
    
        if gen_start is None: gen_start = default_start
        if check_alive is None: check_alive = self._default_check
        if find_neighbors is None: find_neighbors = self._default_neighbors
        self.width = width
        self.height = height
        self.data = gen_start() #could potentially not be 0 or 1
        self.check_alive = check_alive
        self.find_neighbors = find_neighbors

    def _default_neighbors(self, row, col):
        def norm_idx(idx, row=True): # allows for wraparound
            if idx < 0 and row:
                return idx + self.height
            elif idx < 0 and not row:
                return idx + self.width
            elif idx >= self.height and row:
                return idx % self.height
            elif idx >= self.width and not row:
                return idx % self.width
            else:
                return idx

        def neighbor_val(p_row, p_col):
            return self.data[norm_idx(p_row)][norm_idx(p_col, False)]
        
        mods = [-1, 0, 1] #assume square grid
        look = [ neighbor_val(row+rmod, col+cmod) for rmod in mods for cmod in mods \
            if rmod!=0 or cmod!=0 ] #exclude spot

        return sum(look) #assume 1 or 0 val, could change

    def _default_check(self, spot, neighbors):
        if spot == 1:
            return 1 if neighbors==2 or neighbors==3 else 0
        else:
            return 1 if neighbors==3 else 0


    def update(self): #updates for one cycle
        def new_alive(row, col):
            return self.check_alive(self.data[row][col], self.find_neighbors(row,col))

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
    def __init__(self, width=10, height=10, start_state=None):
        if start_state is not None: #assume 2x2 grid
            def gen_start():
                return start_state
            width = len(start_state[0])
            height = len(start_state)
            self.board = Board(width, height, gen_start)
        else:
            self.board = Board(width, height) #add later

    @staticmethod
    def read_start(file_name):
        with open(file_name, 'r') as reading:
            values = [ [int(char) for char in line if char=='0' or char=='1'] for line in reading]
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

    # test = Game(start_state=alive_board(3, 5))
    init_state1 = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]
    init_state2 = [
        [0,0,0,0],
        [0,0,1,0],
        [0,1,1,0],
        [0,0,0,0]
    ]
    test = Game(start_state=init_state2)
    test.loop(1)