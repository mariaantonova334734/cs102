import copy
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        self.grid = self.create_grid(True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            self.grid = self.get_next_generation()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            return [
                [random.randint(0, 1) for _ in range(self.cell_width)]
                for _ in range(self.cell_height)
            ]
        else:
            return [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for pos_of_height in range(self.cell_height):
            for pos_of_width in range(self.cell_width):
                rect = pygame.Rect(
                    self.cell_size * pos_of_width,
                    self.cell_size * pos_of_height,
                    self.cell_size,
                    self.cell_size,
                )
                if self.grid[pos_of_height][pos_of_width]:
                    pygame.draw.rect(self.screen, pygame.Color("yellow"), rect)
                else:
                    pygame.draw.rect(self.screen, pygame.Color("red"), rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        row, col = cell
        neighbours = []
        for pos_of_row in range(max(0, row - 1), min(self.cell_height, row + 2)):
            for pos_of_col in range(max(0, col - 1), min(self.cell_width, col + 2)):
                if not (row == pos_of_row and col == pos_of_col):
                    neighbours += [self.grid[pos_of_row][pos_of_col]]
        return neighbours

    def get_next_generation(self) -> Grid:
        """

        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_gen = copy.deepcopy(self.grid)
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                cell = (row, col)
                summ_of_neighbours = sum(self.get_neighbours(cell))
                if self.grid[row][col] == 1:
                    if summ_of_neighbours == 3 or summ_of_neighbours == 2:
                        new_gen[row][col] = 1
                    else:
                        new_gen[row][col] = 0
                else:
                    if summ_of_neighbours == 3:
                        new_gen[row][col] = 1
                    else:
                        new_gen[row][col] = 0
        return new_gen
