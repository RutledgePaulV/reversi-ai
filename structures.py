import numpy as np

from enums import *



#defines a game board
class Board(object):
    FLAGS = ['external_loop']

    #constructor
    def __init__(self, dimension=8):

        #defining numpy data type
        self.cell_type = np.dtype([('row', int), ('col', int), ('color', int)])

        #constructing empty numpy array to hold cells
        self.table = np.empty((dimension, dimension), dtype=self.cell_type)

        #dimension represents number of rows and columns on the board
        self.dimension = dimension

        #creating new cells in table
        self.__reset__()


    def __reset__(self):

        iterator = np.nditer(self.table, flags=['multi_index'], op_flags=['readwrite'])

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


    #this property returns a list containing all the cells
    @property
    def cells(self):
        return self.filter_all(lambda x: True)


    #this static method returns the direction that must be traveled to move from cell1 to cell2
    @staticmethod
    def get_direction(cell1, cell2):
        return cell2['row'] - cell1['row'], cell2['col'] - cell1['col']


    #checks if two cells are neighbors
    @staticmethod
    def is_neighbor(cell1, cell2):
        net_row = abs(cell1['row'] - cell2['row'])
        net_col = abs(cell1['col'] - cell2['col'])
        return (not (net_row == 0 and net_col == 0)) and (net_row <= 1 and net_col <= 1)


    #checks if a position is within the bounds of the game board
    def in_bounds(self, row, col):
        return (0 <= row < self.dimension) and (0 <= col < self.dimension)


    #filters all cells according to some predicate
    def filter_all(self, predicate):
        return [cell for cell in np.nditer(self.table, flags=self.FLAGS, op_flags=['readwrite'])[0] if predicate(cell)]


    #returns all cells nearby another cell who have no color assigned
    def get_unused_neighbors(self, cell):
        return self.filter_all(lambda cell2: self.is_neighbor(cell, cell2) and
                                             Color.from_int(cell2['color']) is Color.blank)


    #returns all cells nearby another cell who have a color assigned
    def get_used_neighbors(self, cell):
        return self.filter_all(lambda cell2: self.is_neighbor(cell, cell2) and
                                             Color.from_int(cell2['color']) is not Color.blank)


    #returns all cells assigned a color on the game board
    def get_used(self):
        return self.filter_all(lambda cell: Color.from_int(cell['color']) is not Color.blank)


    #returns all cells not assigned a color on the game board
    def get_unused(self):
        return self.filter_all(lambda cell: Color.from_int(cell['color']) is Color.blank)


    #returns all the cells of a given color
    def get_color(self, color):
        return self.filter_all(lambda cell: Color.from_int(cell['color']) is color)


    #checks if a particular cell is a viable move for a particular color
    def check_possible(self, cell, color):

        #cells which will be flipped if the move is played
        effected = []

        #gets all neighboring occupied cells of the opposite color (to be captured)
        neighboring = [x for x in self.get_used_neighbors(cell)
                       if Color.from_int(x['color']) is Color.opposite(color)]

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

                #have not yet found an empty cell or an end point
                found_end = found_empty = False

                #initial positions
                queue, row, col = [], testing['row'], testing['col']

                #while no end condition has been satisfied
                while (not found_end) and (not found_empty) and self.in_bounds(row, col):
                    #keeping track of a queue of all the cells in this direction
                    queue.append(testing)

                    #move to the next cell in the direction
                    testing = self.table[row, col]

                    #check if ending cell has been found (validates move)
                    found_end = Color.from_int(testing['color']) is color

                    #checks if empty cell was found
                    found_empty = Color.from_int(testing['color']) is Color.blank

                    #moving to next position
                    row += direction[0]
                    col += direction[1]

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
        return [x for x in self.get_unused() if self.check_possible(x, color)[0]]


    #steps forward one iteration based on a particular color who is moving and a particular strategy
    def step_forward(self, heuristic, color):
        ranked,available = [], self.get_moves(color)
        for move in available:
            next_board = self.copy()
            next_board.make_move(move, color)
            ranked.append((heuristic.eval(next_board, color), next_board))
        return sorted(ranked, key=lambda x: x[0], reverse=True)[0][1]


    #makes a move on the board
    def make_move(self, cell, color):
        valid, effected = self.check_possible(cell, color)
        if valid:
            self.table[cell['row'], cell['col']]['color'] = color.value
            for each in effected: each['color'] = color.value
        else:
            raise Exception('Move attempted is not valid.')


    #creates a copy of the given board to instantiate new references to cells for constructing trees
    def copy(self):
        b = Board(self.dimension)
        iterator = np.nditer(self.table)
        while not iterator.finished:
            cell = iterator[0]
            row, col = cell['row'], cell['col']
            b.table[row, col] = (row, col, cell['color'])
            iterator.iternext()
        return b