from graphics import *
from enums import *


class Renderer(object):

    def __init__(self, pixels, background):
        self.grid = []
        self.cells = []
        self.board = None
        self.pixels = pixels
        self.window = GraphWin('Render', pixels, pixels)
        self.window.setBackground(background)


    def clear(self):
        self.grid.clear()
        self.cells.clear()


    def hang(self):
        self.window.getMouse()


    def load(self, board):

        self.clear()

        spacing = self.pixels / board.dimension

        for x in range(1, board.dimension):
            coordinate = x * spacing
            self.grid.append(Line(Point(coordinate, 0), Point(coordinate, self.pixels)))
            self.grid.append(Line(Point(0, coordinate), Point(self.pixels, coordinate)))

        radius = 0.35 * spacing

        for cell in board.cells:

            row, column, color = cell['row'], cell['col'], cell['color']
            x = (row + 0.5) * spacing
            y = (column + 0.5) * spacing

            circle = Circle(Point(x, y), radius)
            fill = Color.from_int(color)

            if fill is not Color.blank:
                circle.setFill(fill.name)
                circle.setOutline(fill.name)
                self.cells.append(circle)


    def refresh(self, await=None):
        [line.undraw() for line in self.grid]
        [cell.undraw() for cell in self.cells]
        self.render(await)


    def render(self, await=None):
        [line.draw(self.window) for line in self.grid]
        [cell.draw(self.window) for cell in self.cells]
        if not await:
            self.window.getMouse()
        else:
            await()


    def to_image(self):
        pass