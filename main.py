from weightings import *
from strategy import *
from game import *

heuristic = Weighted(CornerEdgeOther(3,2,1).gen(8))
game = Standard(heuristic)
game.animate(0.5)