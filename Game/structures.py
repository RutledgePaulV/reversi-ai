from itertools import chain, product

from enum import Enum

from graphics import *


class Color(Enum):
    blank = 0
    white = 1
    black = 2

    @staticmethod
    def opposite(color):
        if color is Color.black:
            return Color.white
        elif color is Color.white:
            return Color.black
        else:
            return Color.blank

class Drawable(object):
    def get_drawables(self):
        """
        :rtype : collections.Iterable
        """
        pass

    def draw(self, window):
        for drawable in self.get_drawables():
            drawable.draw(window)


class Board(Drawable):
    def __init__(self, dimension=8, pixels=400):
        self.rows, self.columns, self.cells = {}, {}, []
        self.grid_lines = []
        self.pixels = pixels
        self.dimension = dimension
        self.spacing = (self.pixels / self.dimension)
        self.radius = 20

        #generating cells
        for row, col in product(range(self.dimension), range(self.dimension)):

            x = (col * self.spacing) + 0.5 * self.spacing
            y = (row * self.spacing) + 0.5 * self.spacing
            circle = Circle(Point(x, y), self.radius)
            cell = Cell(row, col, circle, Color.blank)

            if not row in self.rows:
                self.rows[row] = []
            if not col in self.columns:
                self.columns[col] = []

            self.rows[row].append(cell)
            self.columns[col].append(cell)
            self.cells.append(cell)

        #generating grid lines
        for count in range(1, self.dimension):
            coordinate = count * self.spacing
            horizontal_line = Line(Point(coordinate, 0), Point(coordinate, self.pixels))
            vertical_line = Line(Point(0, coordinate), Point(self.pixels, coordinate))
            self.grid_lines.extend([horizontal_line, vertical_line])

    @staticmethod
    def get_direction(cell1, cell2):
        return (cell2.column - cell1.column, cell2.row - cell1.row)

    def get_neighboring(self, cell):
        for row, col in product(range(-1, 2), range(-1, 2)):
            if not ((row == 0) and (col == 0)):
                if (self.dimension > cell.row + row >= 0) and (self.dimension > cell.column + col >= 0):
                    yield self.rows[cell.row + row][cell.column + col]

    def get_unused_neighbors(self, cell):
        return [x for x in self.get_neighboring(cell) if x.color is Color.blank]

    def get_used_neighbors(self, cell):
        return [x for x in self.get_neighboring(cell) if x.color is not Color.blank]

    def get_used(self):
        return [cell for cell in self.cells if cell.color is not Color.blank]

    def get_unused(self):
        return [cell for cell in self.cells if cell.color is Color.blank]

    def get_white(self):
        return [cell for cell in self.cells if cell.color is Color.white]

    def get_black(self):
        return [cell for cell in self.cells if cell.color is Color.black]

    def get_moves(self, color):
        #getting the opposite color
        opposite = Color.opposite(color)

        #getting all unused positions on game board
        possibles = self.get_unused()

        print(len(possibles))

        #for each unused cell
        for cell in possibles:

            #get used cells nearby who are of the opposite color
            used = [x for x in self.get_used_neighbors(cell) if x.color is opposite]

            #if no used cells nearby of opposite color, it is no longer a valid possibility
            if len(used) == 0:
                possibles.remove(cell)
                print("REMOVING: {0}".format(cell))

            #otherwise
            else:

                tests = []

                #for each cell of the opposite color nearby the cell of interest
                for other in used:

                    #get the direction from the cell of interest
                    direction = Board.get_direction(cell,other)

                    #second reference to the cell in the direction
                    cell2 = other

                    valid = False

                    #proceeding in that direction until it runs off board
                    while (cell2.color is not color) and (cell2.color is not Color.blank) and (0 <= cell2.row + direction[0] < self.dimension) and (0 <= cell2.column + direction[1] < self.dimension):
                        cell2 = self.rows[cell2.row + direction[0]][cell2.column + direction[1]]
                        if cell2.color == color:
                            valid = True
                            break

                    tests.append(valid)

                if not any(tests):
                    possibles.remove(cell)

        print(len(possibles))

        return possibles



    #returns this objects drawable components
    def get_drawables(self):
        return self.grid_lines + list(chain.from_iterable([cell.get_drawables() for cell in self.get_used()]))

    def copy(self):
        b = Board(self.dimension)
        [b.cells[index].append(cell.copy()) for index, cell in enumerate(self.cells)]
        return b


class Cell(Drawable):
    def __init__(self, row, column, circle, color):
        self.row = row
        self.column = column
        self.color = color
        self.circle = circle

    def get_drawables(self):
        self.circle.setFill(self.color.name)
        return [self.circle]

    def copy(self):
        return Cell(self.row, self.column, self.circle, self.color)

    def __str__(self):
        return "row: {0}, col: {1}, color: {2}".format(self.row, self.column, self.color.name)