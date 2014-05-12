from structures import *
from strategy import *
from renderer import *
from weightings import *

b = Board()

g = Renderer(500, 'grey')
g.load(b)
g.render()

color = Color.white
weight_gen = CornerEdgeOther(3,2,1)
heuristic = Weighted(weight_gen.gen(b.dimension))

while True:
    b = b.step_forward(heuristic, color)
    color = Color.opposite(color)
    g.load(b)
    g.refresh()

