from itertools import product
import numpy as np

class BaseWeighting(object):

    def __init__(self):
        pass

    def gen(self, dimension):
        pass

class CornerEdgeOther(BaseWeighting):

    def __init__(self, corner, edge, other):
        self.corner = corner
        self.edge = edge
        self.other = other
        super().__init__()

    def gen(self, dimension):

        dimension, edges = dimension-1, []
        corners = [(row,col) for row,col in product((0,dimension),(0,dimension))]
        other = [(row,col) for row,col in product((1,dimension-1),(1,dimension-1))]
        for x in range(1,dimension):
            edges.append((0,x))
            edges.append((x,0))
            edges.append((dimension,x))
            edges.append((x,dimension))


        weights = np.ones((dimension,dimension),float)

        for x,y in corners:
            weights[x,y] = self.corner

        for x,y in edges:
            weights[x,y] = self.edge

        for x,y in other:
            weights[x,y] = self.other

        return weights