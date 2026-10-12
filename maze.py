import random
import time

from cell import Cell
from graphics import Window


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: float,
        cell_size_y: float,
        win: Window | None = None,
        seed: int | None = None,
    ) -> None:
        self.__cells: list[list[Cell]] = []
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        if seed is not None:
            random.seed(seed)

        self.__create_cells()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self) -> None:
        for i in range(self.__num_cols):
            col_cells: list[Cell] = []
            for j in range(self.__num_rows):
                col_cells.append(Cell(self.__win))
            self.__cells.append(col_cells)
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)
        self.__break_entrance_and_exit()

    def __break_entrance_and_exit(self) -> None:
        last_col = self.__num_cols - 1
        last_row = self.__num_rows - 1

        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)

        self.__cells[last_col][last_row].has_bottom_wall = False
        self.__draw_cell(last_col, last_row)

    def __break_walls_r(self, i: int, j: int) -> None:
        current = self.__cells[i][j]
        current.visited = True
        while True:
            to_visit: list[tuple[int, int]] = []
            if i > 0 and not self.__cells[i - 1][j].visited:
                to_visit.append((i - 1, j))
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                to_visit.append((i + 1, j))
            if j > 0 and not self.__cells[i][j - 1].visited:
                to_visit.append((i, j - 1))
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                to_visit.append((i, j + 1))

            if not to_visit:
                self.__draw_cell(i, j)
                return

            next_i, next_j = random.choice(to_visit)
            chosen = self.__cells[next_i][next_j]

            if next_i == i + 1:
                current.has_right_wall = False
                chosen.has_left_wall = False
            elif next_i == i - 1:
                current.has_left_wall = False
                chosen.has_right_wall = False
            elif next_j == j + 1:
                current.has_bottom_wall = False
                chosen.has_top_wall = False
            else:
                current.has_top_wall = False
                chosen.has_bottom_wall = False

            self.__break_walls_r(next_i, next_j)

    def __reset_cells_visited(self) -> None:
        for column in self.__cells:
            for cell in column:
                cell.visited = False

    def solve(self) -> bool:
        return self.__solve_r(0, 0)

    def __solve_r(self, i: int, j: int) -> bool:
        self.__animate()
        current = self.__cells[i][j]
        current.visited = True

        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        directions = (
            (i - 1, j, current.has_left_wall),
            (i + 1, j, current.has_right_wall),
            (i, j - 1, current.has_top_wall),
            (i, j + 1, current.has_bottom_wall),
        )
        for next_i, next_j, blocked in directions:
            if blocked:
                continue
            if not (0 <= next_i < self.__num_cols and 0 <= next_j < self.__num_rows):
                continue
            chosen = self.__cells[next_i][next_j]
            if chosen.visited:
                continue

            current.draw_move(chosen)
            if self.__solve_r(next_i, next_j):
                return True
            current.draw_move(chosen, undo=True)

        return False

    def __draw_cell(self, i: int, j: int) -> None:
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self) -> None:
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.01)
