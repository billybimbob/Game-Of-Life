from time import sleep
from lifegame import Game, no_wrap_neighbors
import curses

def main(stdscr):

    def curses_render(board_info):
        stdscr.clear()
        stdscr.addstr(board_info)
        stdscr.refresh()

    init_state2 = [
        [0,0,0,0],
        [0,0,1,0],
        [0,1,1,0],
        [0,0,0,0]
    ]
    #test = Game(start_state=init_state1, neighbors=no_wrap_neighbors)

    stdscr.nodelay(True)
    stdscr.move(0, 0)
    args = Game.parse_arguements()
    start = Game.read_start(args.file) if args.file else init_state2

    test = Game(start_state=start, render=curses_render) #could put to args
    #test = Game(start_state=start, neighbors=no_wrap_neighbors, render=curses_render)
    while stdscr.getch()==curses.ERR:
        test.run()
        sleep(0.2)


if __name__ == "__main__":
    curses.wrapper(main)