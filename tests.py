import unittest

from cell import Cell
from maze import Maze


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
        # more rows than columns, so a swapped i/j would show up here
        m1 = Maze(0, 0, 7, 3, 10, 10)
        self.assertEqual(len(m1._Maze__cells), 3)
        for column in m1._Maze__cells:
            self.assertEqual(len(column), 7)

    def test_maze_cells_are_distinct_objects(self):
        # guards against [[Cell()] * rows] * cols style aliasing
        m1 = Maze(0, 0, 3, 3, 10, 10)
        cells = [cell for column in m1._Maze__cells for cell in column]
        self.assertEqual(len({id(cell) for cell in cells}), 9)

    def test_maze_cell_positions(self):
        # origin (5, 20), cells 10 wide and 4 tall; cell [2][1] is col 2, row 1
        m1 = Maze(5, 20, 3, 4, 10, 4)
        cell = m1._Maze__cells[2][1]
        self.assertEqual(cell._Cell__x1, 25)
        self.assertEqual(cell._Cell__y1, 24)
        self.assertEqual(cell._Cell__x2, 35)
        self.assertEqual(cell._Cell__y2, 28)

    def test_break_entrance_and_exit(self):
        m1 = Maze(0, 0, 4, 3, 10, 10)
        cells = m1._Maze__cells
        entrance, exit_ = cells[0][0], cells[-1][-1]

        self.assertFalse(entrance.has_top_wall)
        self.assertFalse(exit_.has_bottom_wall)

        # only those two walls are gone
        self.assertTrue(entrance.has_bottom_wall)
        self.assertTrue(entrance.has_left_wall)
        self.assertTrue(entrance.has_right_wall)
        self.assertTrue(exit_.has_top_wall)
        self.assertTrue(exit_.has_left_wall)
        self.assertTrue(exit_.has_right_wall)

        # an interior cell is untouched
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
        # entrance and exit are the same cell
        m1 = Maze(0, 0, 1, 1, 10, 10)
        cell = m1._Maze__cells[0][0]
        self.assertFalse(cell.has_top_wall)
        self.assertFalse(cell.has_bottom_wall)

    def test_cell_without_window_does_not_draw(self):
        c = Cell()
        c.draw(0, 0, 10, 10)
        c.draw_move(Cell())


if __name__ == "__main__":
    unittest.main()
