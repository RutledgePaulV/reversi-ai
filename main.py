from weightings import *
from strategy import *
from game import *

heuristic1 = Weighted(CornerEdgeOther(10,4,1).gen(8))
heuristic2 = Greedy()
game = Standard(heuristic1,heuristic2)
game.animate(0.1)
