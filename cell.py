from graphics import Line, Point, Window


class Cell:
    def __init__(self, win: Window | None = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
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
        if self.__win is None:
            return
        missing = (
            (self.has_top_wall, Point(x1 + 1, y1), Point(x2 - 1, y1)),
            (self.has_bottom_wall, Point(x1 + 1, y2), Point(x2 - 1, y2)),
            (self.has_left_wall, Point(x1, y1 + 1), Point(x1, y2 - 1)),
            (self.has_right_wall, Point(x2, y1 + 1), Point(x2, y2 - 1)),
        )
        for present, start, end in missing:
            if not present:
                self.__win.draw_line(Line(start, end), self.__win.bg)

        walls = (
            (self.has_top_wall, Point(x1, y1), Point(x2, y1)),
            (self.has_bottom_wall, Point(x2, y2), Point(x1, y2)),
            (self.has_left_wall, Point(x1, y2), Point(x1, y1)),
            (self.has_right_wall, Point(x2, y1), Point(x2, y2)),
        )
        for present, start, end in walls:
            if present:
                self.__win.draw_line(Line(start, end), "white")

    def draw_move(self, to_cell: "Cell", undo: bool = False):
        if self.__win is None:
            return
        color = "gray" if undo else "red"
        self_center = Point((self.__x1 + self.__x2) / 2, (self.__y1 + self.__y2) / 2)
        to_center = Point(
            (to_cell.__x1 + to_cell.__x2) / 2, (to_cell.__y1 + to_cell.__y2) / 2
        )
        self.__win.draw_line(Line(self_center, to_center), color)
