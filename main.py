from structures import *
from strategy import *
from renderer import *

b = Board()
BACKGROUND = 'grey'

g = Renderer(500,BACKGROUND)

g.load(b)
g.render()


# result = step_forward(b,standard,Color.white)
#
# result.draw(WINDOW)

result = b.get_neighboring((3,3,1))
