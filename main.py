from structures import *
from strategy import *
from renderer import *

b = Board()

g = Renderer(500,'grey')
g.load(b)
g.render()

color = Color.white
result = b

while True:
    result = step_forward(result,standard,color)
    g.load(result)
    g.refresh()
    color = Color.opposite(color)

