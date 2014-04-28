
#standard heuristic just counts number by color
def standard(board, color):
    return len([cell for cell in board.cells if cell.color is color])

def step_forward(board, heuristic, color):
    available = board.get_moves(color)
    next_boards = [board.copy().make_move(move, color, False) for move in available]
    ranked = [(heuristic(next_board, color),next_board) for next_board in next_boards]
    sorted(ranked,lambda x: x[0])
    return ranked[0]
