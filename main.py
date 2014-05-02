from structures import *
from strategy import *
from renderer import *

b = Board()
g = Renderer(500,'grey')

g.load(b)
g.render()