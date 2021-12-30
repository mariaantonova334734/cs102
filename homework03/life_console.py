import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

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
        curses.endwin()
