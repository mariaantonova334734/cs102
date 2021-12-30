import curses
import curses.ascii
import pathlib
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife, saving: pathlib.Path) -> None:
        super().__init__(life)
        self.saving = saving

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border()

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for pos_in_row in range(self.life.rows):
            for pos_in_col in range(self.life.cols):
                if self.life.curr_generation[pos_in_row][pos_in_col] == 1:
                    screen.addch(pos_in_row + 1, pos_in_col + 1, "*")
                else:
                    screen.addch(pos_in_row + 1, pos_in_col + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()
        curses.noecho()
        screen.clear()  # type: ignore
        screen.refresh()  # type: ignore
        window = curses.newwin(self.life.rows + 2, self.life.cols + 2)
        self.draw_borders(window)
        window.timeout(1)
        window.nodelay(True)
        running = True
        pause = False
        while running:
            current_element = window.getch()
            if current_element == ord("\n"):
                pause = False
            elif current_element == ord("S"):
                self.life.save(self.saving)
            elif current_element == curses.ascii.ESC:
                running = False
            if not pause:
                self.draw_grid(window)
                window.refresh()
                self.life.step()
                time.sleep(2)
        curses.endwin()
