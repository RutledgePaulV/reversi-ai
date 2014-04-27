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
move =  b.get_moves(Color.white)[0]
b.make_move(move,Color.white)

moves = b.get_moves(Color.black)
for move in moves:
    move.color = Color.red
    move.draw(WINDOW)

b.redraw(WINDOW)


WINDOW.getMouse()
WINDOW.close()