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
        [x1, y1, x2, y2] = [self.point1.x, self.point1.y, self.point2.x, self.point2.y]
        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)


class Window:
    def __init__(self, width: int, height: int, bg: str = "gray"):
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

    win.wait_for_close()


if __name__ == "__main__":
    main()
