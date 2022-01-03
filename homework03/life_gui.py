from pathlib import Path

import pygame
from life import GameOfLife
from pygame.locals import *
from ui import 


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen_size = self.width, self.height

        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        for x_position in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x_position, 0), (x_position, self.height))
        for y_position in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y_position), (self.width, y_position))

    def draw_grid(self) -> None:
        for pos_of_rows in range(self.life.rows):
            for pos_of_cols in range(self.life.cols):
                rect = pygame.Rect(
                    self.cell_size * pos_of_cols,
                    self.cell_size * pos_of_rows,
                    self.cell_size,
                    self.cell_size,
                )
                if self.life.curr_generation[pos_of_rows][pos_of_cols]:
                    pygame.draw.rect(self.screen, pygame.Color("green"), rect)
                else:
                    pygame.draw.rect(self.screen, pygame.Color("red"), rect)

    def run(self) -> None:
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        is_game_running = True
        is_game_in_pause = False
        while is_game_running:
            if self.life.is_max_generations_exceeded or  not self.life.is_changing:
                is_game_running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        is_game_running = False
                    elif event.key == pygame.K_SPACE:
                        is_game_in_pause = not is_game_in_pause
                    elif event.key == pygame.K_DOWN:
                        self.life.save(Path("Game_of_life.txt"))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_position = pygame.mouse.get_pos()
                    x_position, y_position = (
                        click_position[1] // self.cell_size,
                        click_position[0] // self.cell_size,
                    )
                    self.life.curr_generation[x_position][y_position] = 1 - self.life.curr_generation[x_position][y_position]
            self.draw_lines()
            self.draw_grid()
            if not is_game_in_pause:
                self.life.step()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

if __name__ == "__main__":
    life = GameOfLife((30, 30), randomize=True)
    gui = GUI(life, 10, 50)
    gui.run()
