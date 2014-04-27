from Game.structures import *

b = Board()
b.rows[3][3].color = Color.white
b.rows[3][4].color = Color.black
b.rows[4][3].color = Color.black
b.rows[4][4].color = Color.white

BACKGROUND = 'grey'
WINDOW = GraphWin('Reversi', b.pixels, b.pixels)
WINDOW.setBackground(BACKGROUND)
b.draw(WINDOW)

#drawing all possible first moves for white
for x in b.get_moves(Color.black):
    x.color = Color.red
    x.draw(WINDOW)

WINDOW.getMouse()
WINDOW.close()