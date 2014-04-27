from Game.structures import *

b = Board()
b.rows[3][3].color = Color.white
b.rows[3][4].color = Color.black
b.rows[4][3].color = Color.black
b.rows[4][4].color = Color.white

white_moves = b.get_moves(Color.white)
[print(move) for move in white_moves]

BACKGROUND = 'grey'
WINDOW = GraphWin('Reversi', b.pixels, b.pixels)
WINDOW.setBackground(BACKGROUND)
b.draw(WINDOW)

WINDOW.getMouse()
WINDOW.close()