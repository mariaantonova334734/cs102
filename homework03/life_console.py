import curses
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
                    screen.addch(pos_in_row + 1, pos_in_col + 1, "■")
                else:
                    screen.addch(pos_in_row + 1, pos_in_col + 1, " ")

    def run(self) -> None:
        screen_in_game = curses.initscr()
        curses.noecho()
        screen_in_game.clear()  # type: ignore
        screen_in_game.refresh()  # type: ignore
        window_in_game = curses.newwin(self.life.rows + 2, self.life.cols + 2)
        self.draw_borders(window_in_game)
        window_in_game.timeout(1)
        window_in_game.nodelay(True)
        running_of_game = True
        pause = False
        while running_of_game:
            current_element = window_in_game.getch()
            if current_element == ord("\n") or current_element == ord(" "):
                pause = not pause
            elif current_element == ord("S") or current_element == ord("s"):
                self.life.save(self.saving)
            elif current_element == ord("Q") or current_element == ord("q"):
                running_of_game = False
            if not pause:
                self.draw_grid(window_in_game)
                window_in_game.refresh()
                self.life.step()
                time.sleep(2)
        curses.endwin()