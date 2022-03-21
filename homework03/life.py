import copy
import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [
                [random.randint(0, 1) for _ in range(self.cols)]
                for _ in range(self.rows)
            ]
        else:
            return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        row1, col1 = cell
        res_neighbour = []
        for row_position in range(row1 - 1, row1 + 2):
            for col_position in range(col1 - 1, col1 + 2):
                flag = True
                if row_position < 0 or row_position >= self.rows:
                    flag = False
                if col_position < 0 or col_position >= self.cols:
                    flag = False
                if row_position == row1 and col_position == col1:
                    flag = False
                if flag:
                    res_neighbour.append(
                        self.curr_generation[row_position][col_position]
                    )
        return res_neighbour

    def get_next_generation(self) -> Grid:
        next_gen = copy.deepcopy(self.curr_generation)
        for row in range(self.rows):
            for col in range(self.cols):
                cell = (row, col)
                summ_of_neighbours = sum(self.get_neighbours(cell))
                if summ_of_neighbours < 2 or summ_of_neighbours > 3:
                    next_gen[row][col] = 0
                elif summ_of_neighbours == 3:
                    next_gen[row][col] = 1
        return next_gen

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, encoding="utf-8") as file_input:
            input_list = file_input.read().splitlines()
            grid = [[int(cell) for cell in row] for row in input_list]
            # for row in input_list:
            #     line = []
            #     for cell in row:
            #         line.append(int(cell))
            #     grid.append(line)
            # file_input.close()
            game_of_life = GameOfLife((len(grid), len(grid[0])))
            game_of_life.curr_generation = grid
        return game_of_life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="utf-8") as file_input:
            for row in self.curr_generation:
                for cell in row:
                    file_input.write(str(cell))
                file_input.write("\n")
        # file_input.close()
