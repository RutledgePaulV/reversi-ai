from itertools import chain, product

from enum import Enum

from graphics import *

#color enum represents color of each game piece
class Color(Enum):
    blank = 0
    white = 1
    black = 2
    red = 3


    #method on enum allows getting the opposite color (could have used booleans)
    @staticmethod
    def opposite(color):
        if color is Color.black:
            return Color.white
        elif color is Color.white:
            return Color.black
        else:
            return color


#represents an object that can be drawn
class Drawable(object):

    #returns any sub components which are drawable
    def get_drawables(self):
        """
        :rtype : collections.Iterable
        """
        pass


    #draws each sub component to the provided context
    def draw(self, context):
        for drawable in self.get_drawables():
            drawable.draw(context)


#defines a game board
class Board(Drawable):

    #constructor
    def __init__(self, dimension=8, pixels=400):

        #various containers for easy access of cells
        self.rows, self.columns, self.cells = {}, {}, []

        #some sub components for drawing grid lines on context
        self.grid_lines = []

        #number of pixels that define the board graphically
        self.pixels = pixels

        #dimension represents number of rows and columns on the board
        self.dimension = dimension

        #calculating spacing between each row / column
        self.spacing = (self.pixels / self.dimension)

        #radius of each piece on the game baord
        self.radius = 0.35 * self.spacing

        #generating cells
        for row, col in product(range(self.dimension), range(self.dimension)):

            #defining x position
            x = (col * self.spacing) + 0.5 * self.spacing

            #defining y position
            y = (row * self.spacing) + 0.5 * self.spacing

            #defining graphical representation
            circle = Circle(Point(x, y), self.radius)

            #creating actual cell object
            cell = Cell(row, col, circle, Color.blank)

            #if the current row doesn't exist yet, create it
            if not row in self.rows:
                self.rows[row] = []

            #if the current column doesn't exist yet, create it
            if not col in self.columns:
                self.columns[col] = []

            #appending cell to various containers
            self.rows[row].append(cell)
            self.columns[col].append(cell)
            self.cells.append(cell)

        #generating grid lines
        for count in range(1, self.dimension):

            #getting distance in pixels from top left
            coordinate = count * self.spacing

            #constructing horizontal grid line
            horizontal_line = Line(Point(coordinate, 0), Point(coordinate, self.pixels))

            #constructing vertical grid line
            vertical_line = Line(Point(0, coordinate), Point(self.pixels, coordinate))

            #adding grid lines to list of grid lines
            self.grid_lines.extend([horizontal_line, vertical_line])


    #this static method returns the direction that must be traveled to move from cell1 to cell2
    @staticmethod
    def get_direction(cell1, cell2):
        return cell2.row - cell1.row, cell2.column - cell1.column


    #gets any immediate neighbors of a cell (including diagonal), includes check for existence
    def get_neighboring(self, cell):

        #double for loop reduced via itertools.product
        for row, col in product(range(-1, 2), range(-1, 2)):

            #don't need to check the current cell
            if not ((row == 0) and (col == 0)):

                #as long as the position is in the bounds of the game board
                if (self.dimension > cell.row + row >= 0) and (self.dimension > cell.column + col >= 0):

                    #yield the given cell
                    yield self.rows[cell.row + row][cell.column + col]


    #returns all cells nearby another cell who have no color assigned
    def get_unused_neighbors(self, cell):
        return [x for x in self.get_neighboring(cell) if x.color is Color.blank]


    #returns all cells nearby another cell who have a color assigned
    def get_used_neighbors(self, cell):
        return [x for x in self.get_neighboring(cell) if x.color is not Color.blank]


    #returns all cells assigned a color on the game board
    def get_used(self):
        return [cell for cell in self.cells if cell.color is not Color.blank]


    #returns all cells not assigned a color on the game board
    def get_unused(self):
        return [cell for cell in self.cells if cell.color is Color.blank]


    #returns all cells assigned the color white on the board
    def get_white(self):
        return [cell for cell in self.cells if cell.color is Color.white]


    #returns all cells assigned the color black on the board
    def get_black(self):
        return [cell for cell in self.cells if cell.color is Color.black]


    #checks if a particular cell is a viable move for a particular color
    def check_possible(self, cell, color):

        #gets all neighboring occupied cells of the opposite color (to be captured)
        neighboring = [x for x in self.get_used_neighbors(cell) if x.color is Color.opposite(color)]

        #if there are no neighbors of the opposite color, it is not a valid move
        if len(neighboring) == 0:
            return False

        #otherwise
        else:

            #for each neighboring cell
            for neighbor in neighboring:

                #setting a new variable for iteration in the given direction
                testing = neighbor

                #getting the direction from the cell being checked to its neighbor
                direction = Board.get_direction(cell, neighbor)

                #first cell to be checked must be in bounds of the game board
                in_vertical = in_horizontal = True

                #have not yet found an empty cell or an end point
                found_end = found_empty = False

                #while no end condition has been satisfied
                while (not found_end) and (not found_empty) and (in_vertical and in_horizontal):

                    #move to the next cell in the direction
                    testing = self.rows[testing.row + direction[0]][testing.column + direction[1]]

                    #check if ending cell has been found (validates move)
                    found_end = testing.color is color

                    #checks if empty cell was found
                    found_empty = testing.color is Color.blank

                    #checks if cell in vertical bounds
                    in_vertical = (0 <= testing.row + direction[0] < self.dimension)

                    #checks if cell in horizontal bounds
                    in_horizontal = (0 <= testing.column + direction[1] < self.dimension)

                #if an end point was found then we have validated the position
                if found_end:
                    return True

            #if nothing validated or faulted, move is not valid
            return False


    #returns all possible moves for a given color
    def get_moves(self, color):
        return [x for x in self.get_unused()if self.check_possible(x,color)]


    #returns this objects drawable components
    def get_drawables(self):
        return self.grid_lines + list(chain.from_iterable([cell.get_drawables() for cell in self.get_used()]))


    #creates a copy of the given board to instantiate new references to cells for constructing trees
    def copy(self):
        b = Board(self.dimension)
        [b.cells[index].append(cell.copy()) for index, cell in enumerate(self.cells)]
        return b


#defines a cell
class Cell(Drawable):

    #constructor
    def __init__(self, row, column, circle, color):
        self.row = row
        self.column = column
        self.color = color
        self.circle = circle


    #returns drawable sub components
    def get_drawables(self):
        self.circle.setFill(self.color.name)
        return [self.circle]


    #returns a copy of the given cell to create new references
    def copy(self):
        return Cell(self.row, self.column, self.circle, self.color)


    #returns a string representation of the cell
    def __str__(self):
        return "row: {0}, col: {1}, color: {2}".format(self.row, self.column, self.color.name)