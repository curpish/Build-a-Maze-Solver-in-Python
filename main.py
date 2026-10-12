from graphics import Line, Point, Window
from maze import Maze


def main():
    width, height, margin = 800, 600, 10
    win = Window(width, height)

    # outline: top-left -> top-right -> bottom-right -> bottom-left -> back
    corners = [
        Point(margin, margin),
        Point(width - margin, margin),
        Point(width - margin, height - margin),
        Point(margin, height - margin),
    ]
    for start, end in zip(corners, corners[1:] + corners[:1]):
        win.draw_line(Line(start, end), "navy")

    num_rows = 20
    num_cols = 30
    margin = 100
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows

    _maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)

    win.wait_for_close()


if __name__ == "__main__":
    main()
