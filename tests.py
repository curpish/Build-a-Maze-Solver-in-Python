import unittest

from cell import Cell
from maze import Maze


def wall_layout(maze):
    return [
        [
            (c.has_top_wall, c.has_bottom_wall, c.has_left_wall, c.has_right_wall)
            for c in column
        ]
        for column in maze._Maze__cells
    ]


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_create_cells_large(self):
        num_cols = 30
        num_rows = 20
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._Maze__cells), num_cols)
        self.assertEqual(len(m1._Maze__cells[0]), num_rows)

    def test_maze_create_cells_single_cell(self):
        m1 = Maze(0, 0, 1, 1, 10, 10)
        self.assertEqual(len(m1._Maze__cells), 1)
        self.assertEqual(len(m1._Maze__cells[0]), 1)

    def test_maze_create_cells_not_square(self):
        m1 = Maze(0, 0, 7, 3, 10, 10)
        self.assertEqual(len(m1._Maze__cells), 3)
        for column in m1._Maze__cells:
            self.assertEqual(len(column), 7)

    def test_maze_cells_are_distinct_objects(self):
        m1 = Maze(0, 0, 3, 3, 10, 10)
        cells = [cell for column in m1._Maze__cells for cell in column]
        self.assertEqual(len({id(cell) for cell in cells}), 9)

    def test_maze_cell_positions(self):
        m1 = Maze(5, 20, 3, 4, 10, 4)
        cell = m1._Maze__cells[2][1]
        self.assertEqual(cell._Cell__x1, 25)
        self.assertEqual(cell._Cell__y1, 24)
        self.assertEqual(cell._Cell__x2, 35)
        self.assertEqual(cell._Cell__y2, 28)

    def test_break_entrance_and_exit(self):
        m1 = Maze(0, 0, 4, 3, 10, 10)
        cells = m1._Maze__cells

        for column in cells:
            for cell in column:
                cell.has_top_wall = cell.has_bottom_wall = True
                cell.has_left_wall = cell.has_right_wall = True

        m1._Maze__break_entrance_and_exit()

        entrance, exit_ = cells[0][0], cells[-1][-1]
        self.assertFalse(entrance.has_top_wall)
        self.assertFalse(exit_.has_bottom_wall)

        self.assertTrue(entrance.has_bottom_wall)
        self.assertTrue(entrance.has_left_wall)
        self.assertTrue(entrance.has_right_wall)
        self.assertTrue(exit_.has_top_wall)
        self.assertTrue(exit_.has_left_wall)
        self.assertTrue(exit_.has_right_wall)

        middle = cells[1][1]
        self.assertTrue(middle.has_top_wall)
        self.assertTrue(middle.has_bottom_wall)

    def test_break_entrance_and_exit_called_directly(self):
        m1 = Maze(0, 0, 4, 3, 10, 10)
        cells = m1._Maze__cells
        cells[0][0].has_top_wall = True
        cells[-1][-1].has_bottom_wall = True

        m1._Maze__break_entrance_and_exit()

        self.assertFalse(cells[0][0].has_top_wall)
        self.assertFalse(cells[-1][-1].has_bottom_wall)

    def test_break_entrance_and_exit_single_cell(self):
        m1 = Maze(0, 0, 1, 1, 10, 10)
        cell = m1._Maze__cells[0][0]
        self.assertFalse(cell.has_top_wall)
        self.assertFalse(cell.has_bottom_wall)

    def test_maze_cells_not_visited_after_construction(self):
        m1 = Maze(0, 0, 8, 11, 10, 10, seed=0)
        for column in m1._Maze__cells:
            for cell in column:
                self.assertFalse(cell.visited)

    def test_reset_cells_visited(self):
        m1 = Maze(0, 0, 5, 7, 10, 10, seed=0)
        cells = m1._Maze__cells
        for column in cells:
            for cell in column:
                cell.visited = True

        m1._Maze__reset_cells_visited()

        for column in cells:
            for cell in column:
                self.assertFalse(cell.visited)

    def test_reset_cells_visited_keeps_walls(self):
        m1 = Maze(0, 0, 5, 7, 10, 10, seed=0)
        before = wall_layout(m1)
        m1._Maze__reset_cells_visited()
        self.assertEqual(wall_layout(m1), before)

    def test_maze_shared_walls_agree(self):
        m1 = Maze(0, 0, 8, 11, 10, 10, seed=0)
        cells = m1._Maze__cells
        for i in range(11):
            for j in range(8):
                if i + 1 < 11:
                    self.assertEqual(cells[i][j].has_right_wall, cells[i + 1][j].has_left_wall)
                if j + 1 < 8:
                    self.assertEqual(cells[i][j].has_bottom_wall, cells[i][j + 1].has_top_wall)

    def test_maze_is_connected_with_no_loops(self):
        num_cols, num_rows = 11, 8
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)
        cells = m1._Maze__cells

        open_walls = 0
        for i in range(num_cols):
            for j in range(num_rows):
                if i + 1 < num_cols and not cells[i][j].has_right_wall:
                    open_walls += 1
                if j + 1 < num_rows and not cells[i][j].has_bottom_wall:
                    open_walls += 1
        self.assertEqual(open_walls, num_cols * num_rows - 1)

        reached = {(0, 0)}
        stack = [(0, 0)]
        while stack:
            i, j = stack.pop()
            cell = cells[i][j]
            moves = []
            if not cell.has_left_wall:
                moves.append((i - 1, j))
            if not cell.has_right_wall:
                moves.append((i + 1, j))
            if not cell.has_top_wall:
                moves.append((i, j - 1))
            if not cell.has_bottom_wall:
                moves.append((i, j + 1))
            for move in moves:
                if move in reached or not (0 <= move[0] < num_cols and 0 <= move[1] < num_rows):
                    continue
                reached.add(move)
                stack.append(move)
        self.assertEqual(len(reached), num_cols * num_rows)

    def test_maze_outer_walls_intact_except_entrance_and_exit(self):
        num_cols, num_rows = 6, 5
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)
        cells = m1._Maze__cells
        for j in range(num_rows):
            self.assertTrue(cells[0][j].has_left_wall)
            self.assertTrue(cells[-1][j].has_right_wall)
        for i in range(num_cols):
            self.assertEqual(cells[i][0].has_top_wall, i != 0)
            self.assertEqual(cells[i][-1].has_bottom_wall, i != num_cols - 1)

    def test_maze_same_seed_same_layout(self):
        a = Maze(0, 0, 10, 10, 10, 10, seed=42)
        b = Maze(0, 0, 10, 10, 10, 10, seed=42)
        self.assertEqual(wall_layout(a), wall_layout(b))

    def test_maze_different_seed_different_layout(self):
        a = Maze(0, 0, 10, 10, 10, 10, seed=1)
        b = Maze(0, 0, 10, 10, 10, 10, seed=2)
        self.assertNotEqual(wall_layout(a), wall_layout(b))

    def test_maze_solve_returns_true(self):
        for seed in range(10):
            m1 = Maze(0, 0, 8, 11, 10, 10, seed=seed)
            self.assertTrue(m1.solve())

    def test_maze_solve_visits_the_exit(self):
        m1 = Maze(0, 0, 6, 9, 10, 10, seed=3)
        self.assertTrue(m1.solve())
        self.assertTrue(m1._Maze__cells[-1][-1].visited)

    def test_maze_solve_single_cell(self):
        m1 = Maze(0, 0, 1, 1, 10, 10)
        self.assertTrue(m1.solve())

    def test_maze_solve_returns_false_when_sealed(self):
        m1 = Maze(0, 0, 4, 4, 10, 10, seed=0)
        for column in m1._Maze__cells:
            for cell in column:
                cell.has_top_wall = cell.has_bottom_wall = True
                cell.has_left_wall = cell.has_right_wall = True
        self.assertFalse(m1.solve())

    def test_maze_solve_follows_open_walls_only(self):
        m1 = Maze(0, 0, 1, 4, 10, 10, seed=0)
        cells = m1._Maze__cells
        self.assertTrue(m1.solve())
        self.assertTrue(all(column[0].visited for column in cells))

    def test_cell_without_window_does_not_draw(self):
        c = Cell()
        c.draw(0, 0, 10, 10)
        c.draw_move(Cell())


if __name__ == "__main__":
    unittest.main()
