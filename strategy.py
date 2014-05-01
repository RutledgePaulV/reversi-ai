import numpy as np

#standard heuristic just counts number by color
def standard(board, color):
    return len([cell for cell in np.nditer(board.table, flags=board.FLAGS)[0]if cell.color is color])

def step_forward(board, heuristic, color):
    available = board.get_moves(color)
    ranked = []
    for move in available:
        new_board = board.copy()
        new_board.make_move(move, color, False)
        ranked.append((heuristic(new_board, color), new_board))

    sorted(ranked, key=lambda x: x[0])
    return ranked[0][1]
