from tkinter import BOTH, Canvas, Tk


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas: Canvas, fill_color: str = "orange"):
        x1, y1, x2, y2 = self.point1.x, self.point1.y, self.point2.x, self.point2.y
        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)


class Window:
    def __init__(self, width: int, height: int, bg: str = "black"):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, width=width, height=height, bg=bg)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        Tk.update_idletasks(self.__root)
        Tk.update(self.__root)

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.__canvas, fill_color)


class Cell:
    def __init__(self, win: Window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1.0
        self.__x2 = -1.0
        self.__y1 = -1.0
        self.__y2 = -1.0
        self.__win = win

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        if self.has_top_wall:
            self.__win.draw_line(Line(Point(x1, y1), Point(x2, y1)), "white")
        if self.has_bottom_wall:
            self.__win.draw_line(Line(Point(x2, y2), Point(x1, y2)), "white")
        if self.has_left_wall:
            self.__win.draw_line(Line(Point(x1, y2), Point(x1, y1)), "white")
        if self.has_right_wall:
            self.__win.draw_line(Line(Point(x2, y1), Point(x2, y2)), "white")

    def draw_move(self, to_cell: "Cell", undo: bool = False):
        color = "gray" if undo else "red"
        self_center = Point((self.__x1 + self.__x2) / 2, (self.__y1 + self.__y2) / 2)
        to_center = Point(
            (to_cell.__x1 + to_cell.__x2) / 2, (to_cell.__y1 + to_cell.__y2) / 2
        )
        self.__win.draw_line(Line(self_center, to_center), color)

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

    # medium horizontal line centered on the screen
    cx, cy, half = width // 2, height // 2, 100
    win.draw_line(Line(Point(cx - half, cy), Point(cx + half, cy)), "orange")

    # test cells: all walls / no left wall / no top or bottom
    c1 = Cell(win)
    c1.draw(50, 50, 100, 100)

    c2 = Cell(win)
    c2.has_left_wall = False
    c2.draw(100, 50, 150, 100)

    c3 = Cell(win)
    c3.has_top_wall = False
    c3.has_bottom_wall = False
    c3.draw(150, 50, 200, 100)

    # test moves: red forward, gray undo
    c1.draw_move(c2)
    c2.draw_move(c3, undo=True)

    # corridor test: cells with empty space between them
    a = Cell(win)
    a.draw(50, 150, 100, 200)

    b = Cell(win)
    b.draw(200, 150, 250, 200)

    c = Cell(win)
    c.draw(350, 150, 400, 200)

    a.draw_move(b)               # red across the gap
    b.draw_move(c, undo=True)    # gray across the gap

    win.wait_for_close()


if __name__ == "__main__":
    main()
