from structures import *
from strategy import *

b = Board()
BACKGROUND = 'grey'
WINDOW = GraphWin('Reversi', b.pixels, b.pixels)
WINDOW.setBackground(BACKGROUND)

b.draw(WINDOW)
result,effected = b.check_possible(b.table[2,2],Color.white)

print(result)

WINDOW.getMouse()
WINDOW.close()