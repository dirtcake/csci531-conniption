from expand import breadth
from board_class import BoardState
# from evaluate import Evaluator
from cevaluate.evaluate import evaluate_full


# eval = Evaluator()


def max_value(state, alpha, beta, depth):
    # val = eval.evaluate_full(state.board, state.player_turn)
    val = evaluate_full(state.board, state.player_turn)

    if depth == 0 or abs(val) > 500000:
        return val

    v = -2147483648
    for move in breadth(state):
        v = max(v, min_value(move[0], alpha, beta, depth-1))
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v


def min_value(state, alpha, beta, depth):
    # val = eval.evaluate_full(state.board, state.player_turn % 2 + 1)
    val = evaluate_full(state.board, state.player_turn % 2 + 1)

    if depth == 0 or abs(val) > 500000:
        return val

    v = 2147483647
    for move in breadth(state):
        v = min(v, max_value(move[0], alpha, beta, depth-1))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v


def alpha_beta_search(state, depth):
    moves = list(breadth(state))

    moves_evals = [min_value(move[0], -2147483648, 2147483647, depth-1) for move in moves]
    # print(moves_evals)
    return moves[moves_evals.index(max(moves_evals))]


