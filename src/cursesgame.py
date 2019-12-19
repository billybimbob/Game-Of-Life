from lifegame import Game
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

    stdscr.move(0, 0)
    args = Game.parse_arguements()
    start = Game.read_start(args.file) if args.file else init_state2

    test = Game(start_state=start, render=curses_render)
    test.loop(4)


if __name__ == "__main__":
    curses.wrapper(main)