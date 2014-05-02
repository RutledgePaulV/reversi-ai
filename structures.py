from itertools import product

import numpy as np

from enums import *




#defines a game board
class Board(object):
    FLAGS = ['external_loop', 'refs_ok']

    #constructor
    def __init__(self, dimension=8):

        #defining numpy data type
        self.cell_type = np.dtype([('row', int), ('column', int), ('color', int)])

        #constructing empty numpy array to hold cells
        self.table = np.empty((dimension, dimension), dtype=self.cell_type)

        #dimension represents number of rows and columns on the board
        self.dimension = dimension

        #creating new cells in table
        self.__reset__()


    def __reset__(self):

        iterator = np.nditer(self.table, flags=['multi_index', 'refs_ok'], op_flags=['readwrite'])

        while not iterator.finished:
            #getting indices
            row, col = iterator.multi_index

            #creating actual cell object
            self.table[row, col] = (row, col, Color.blank.value)

            #moving iterator
            iterator.iternext()


        #half the dimension
        half = self.dimension // 2

        #half the dimension minus one
        half_less = half - 1

        #setting initial starting positions
        self.table[half, half]['color'] = Color.white.value
        self.table[half_less, half]['color'] = Color.black.value
        self.table[half, half_less]['color'] = Color.black.value
        self.table[half_less, half_less]['color'] = Color.white.value


    #this static method returns the direction that must be traveled to move from cell1 to cell2
    @staticmethod
    def get_direction(cell1, cell2):
        return cell2['row'] - cell1['row'], cell2['column'] - cell1['column']


    #this property returns a list containing all the cells
    @property
    def cells(self):
        return [cell for cell in np.nditer(self.table, flags=self.FLAGS)[0]]


    #gets any immediate neighbors of a cell (including diagonal), includes check for existence
    def get_neighboring(self, cell):
        for row, col in product((-1, 0, 1), (-1, 0, 1)):
            if not ((row == 0) and (col == 0)):
                if (self.dimension > cell['row'] + row >= 0) and (self.dimension > cell['column'] + col >= 0):
                    yield self.table[cell['row'] + row, cell['column'] + col]


    #returns all cells nearby another cell who have no color assigned
    def get_unused_neighbors(self, cell):
        return [x for x in self.get_neighboring(cell) if Color.from_int(x['color']) is not Color.blank]


    #returns all cells nearby another cell who have a color assigned
    def get_used_neighbors(self, cell):
        return [x for x in self.get_neighboring(cell) if Color.from_int(x['color']) is not Color.blank]


    #returns all cells assigned a color on the game board
    def get_used(self):
        return [cell for cell in np.nditer(self.table, flags=self.FLAGS)[0] if
                Color.from_int(cell['color']) is not Color.blank]


    #returns all cells not assigned a color on the game board
    def get_unused(self):
        return [cell for cell in np.nditer(self.table, flags=self.FLAGS)[0] if
                Color.from_int(cell['color']) is Color.blank]


    #returns all cells assigned the color white on the board
    def get_white(self):
        return [cell for cell in np.nditer(self.table, flags=self.FLAGS)[0] if
                Color.from_int(cell['color']) is Color.white]


    #returns all cells assigned the color black on the board
    def get_black(self):
        return [cell for cell in np.nditer(self.table, flags=self.FLAGS)[0] if
                Color.from_int(cell['color']) is Color.black]


    #checks if a particular cell is a viable move for a particular color
    def check_possible(self, cell, color):

        #cells which will be flipped if the move is played
        effected = []

        #gets all neighboring occupied cells of the opposite color (to be captured)
        neighboring = [x for x in self.get_used_neighbors(cell) if Color.from_int(x['color']) is Color.opposite(color)]

        #if there are no neighbors of the opposite color, it is not a valid move
        if len(neighboring) == 0:
            return False, effected

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

                queue = []

                #while no end condition has been satisfied
                while (not found_end) and (not found_empty) and (in_vertical and in_horizontal):
                    queue.append(testing)

                    #move to the next cell in the direction
                    testing = self.table[testing.row + direction[0], testing.column + direction[1]]

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
                    effected.extend(queue)

            #if at least one cell would be effected by the move
            if len(effected) > 0:
                return True, effected

            #if nothing validated or faulted, move is not valid
            else:
                return False, effected


    #returns all possible moves for a given color
    def get_moves(self, color):
        return [x for x in self.get_unused() if self.check_possible(x, color)]


    def make_move(self, cell, color, check=True):
        valid, effected = self.check_possible(cell, color)
        if (not check) or valid:
            for each in effected:
                each.color = color
            cell.color = color
        else:
            return False


    def serialize(self):
        lines = []
        for row in self.table:
            line = ''
            for col in row:
                line += str(self.table[row, col].color.value)
            lines.append(line)
        return '\n'.join(lines)


    #creates a copy of the given board to instantiate new references to cells for constructing trees
    def copy(self):
        b = Board(self.dimension)
        iterator = np.nditer(self.table, flags=['multi_index', 'refs_ok'])
        while not iterator.finished:
            row, col = iterator.multi_index
            b.table[row, col] = iterator[0].copy()
            iterator.iternext()
        return b