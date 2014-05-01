from structures import *
from strategy import *

b = Board()
BACKGROUND = 'grey'
WINDOW = GraphWin('Reversi', b.pixels, b.pixels)
WINDOW.setBackground(BACKGROUND)

b.draw(WINDOW)

result = step_forward(b,standard,Color.white)

result.draw(WINDOW)

WINDOW.getMouse()
WINDOW.close()