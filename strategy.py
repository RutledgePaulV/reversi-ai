from enums import *

#standard heuristic just counts number by color
def standard(board, color):
    return len(board.filter_all(lambda cell: Color.from_int(cell['color']) is color))

#steps forward one iteration based on a particular color who is moving and a particular heuristic weighting
def step_forward(board, heuristic, color):
    ranked = []
    available = board.get_moves(color)
    for move in available:
        new_board = board.copy()
        new_board.make_move(move, color, False)
        ranked.append((heuristic(new_board, color), new_board))
    return sorted(ranked, key=lambda x: x[0], reverse=True)[0][1]
