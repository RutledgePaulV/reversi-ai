from enums import *

#standard heuristic just counts number by color
def standard(board, color):
    return len(board.filter_all(lambda cell: Color.from_int(cell['color']) is color))


def step_forward(board, heuristic, color):
    available = board.get_moves(color)
    ranked = []
    for move in available:
        new_board = board.copy()
        new_board.make_move(move, color, False)
        ranked.append((heuristic(new_board, color), new_board))

    # sorted(ranked, key=lambda x: x[0])

    print(ranked)
    return ranked[0][1]
