from expand import breadth
from board_class import BoardState
from evaluate import Evaluator
# from cevaluate.evaluate import evaluate_full


eval = Evaluator()


def max_value(state, alpha, beta, depth):
    val = eval.evaluate_full(state.board, state.player_turn)
    # val = evaluate_full(state.board, state.player_turn)

    if depth == 0 or abs(val) > 500000:
        if val > 0:
            return val, depth
        return val, 0

    v = -2147483648
    for move in breadth(state):
        hold, win_depth = min_value(move[0], alpha, beta, depth-1)
        v = max(v, hold)
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v, win_depth


def min_value(state, alpha, beta, depth):
    val = eval.evaluate_full(state.board, state.player_turn % 2 + 1)
    # val = evaluate_full(state.board, state.player_turn % 2 + 1)

    if depth == 0 or abs(val) > 500000:
        if val > 0:
            return val, depth
        return val, 0

    v = 2147483647
    for move in breadth(state):
        hold, win_depth = max_value(move[0], alpha, beta, depth-1)
        v = min(v, hold)
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v, win_depth


def alpha_beta_search(state, depth):
    moves = list(breadth(state))

    moves_evals = [min_value(move[0], -2147483648, 2147483647, depth-1) for move in moves]
    depth = 0
    value = None
    for move in moves_evals:
        if move[0] > 500000 and move[1] > depth:
            value = move[0]
            depth = move[1]
    if value is not None:
        return moves[moves_evals.index((value, depth))]
    else:
        return moves[moves_evals.index((max(moves_evals, key=lambda x: x[0])))]


