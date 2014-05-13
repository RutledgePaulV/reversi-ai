from enums import *
import numpy as np

#provides basic structure of a heuristic class
class BaseHeuristic(object):

    def __init__(self):
        pass

    def eval(self, board, color):
        pass


#naive greedy algorithm heuristic, just evaluates
class Greedy(BaseHeuristic):

    def __init__(self):
        super().__init__()

    def eval(self, board, color):
        return len(board.get_color(color))


#this class applies a given initial weighting to the cells of the particular color
#(equivalent to greedy for weighting of 1's)
class Weighted(BaseHeuristic):

    def __init__(self,weights):
        self.weights = weights
        super().__init__()


    def eval(self,board,color):
        return sum([self.weights[cell['row'],cell['col']] for cell in board.get_color(color)])


class Mobility(BaseHeuristic):

    def __init__(self):
        super().__init__()


    def eval(self, board, color):
        pass


class Lookahead(BaseHeuristic):

    def __init__(self, criterion_heuristic):
        self.criterion = criterion_heuristic
        super().__init__()


    def eval(self, board, color):
        pass
