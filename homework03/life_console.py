import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for pos_in_row in range(self.life.rows):
            for pos_in_col in range(self.life.cols):
                if self.life.curr_generation[pos_in_row][pos_in_col] == 1:
                    screen.addch(pos_in_row + 1, pos_in_col + 1, "*")
                else:
                    screen.addch(pos_in_row + 1, pos_in_col + 1, " ")

    #def run(self) -> None:
        screen = curses.initscr()
        curses.noecho()
        screen.clear()
        screen.refresh()
        window = curses.newwin(self.life.rows + 2, self.life.cols + 2)
        self.draw_borders(window)
        window.timeout(1)
        window.nodelay(True)

        running = True
        paused = False
        while running:
            curr_el = window.getch()
            if curr_el == ord("\n"):
                paused = False if paused else True
            elif curr_el == ord("S"):
                self.life.save(self.save_path)
            elif curr_el == curses.ascii.ESC:
                running = False
            if not paused:
                self.draw_grid(window)
                window.refresh()
                self.life.step()

                time.sleep(1)

        curses.endwin()
