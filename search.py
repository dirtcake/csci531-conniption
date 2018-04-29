from expand import breadth
from board_class import BoardState
from cevaluate.evaluate import evaluate_full

def max_value(state, alpha, beta, depth):
    val = evaluate_full(state.board, 1)

    if depth == 0 or abs(val) > 500000:
        return val,

    v = -2147483648
    v_i = 0
    for i, move in enumerate(breadth(state)):
        v2 = min_value(move[0], alpha, beta, depth-1)
        if v2 > v:
            v = v2
            v_i = i
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v, v_i


def min_value(state, alpha, beta, depth):
    val = evaluate_full(state.board, 1)

    if depth == 0 or abs(val) > 500000:
        return val

    v = 2147483647
    for move in breadth(state):
        v = min((v,), max_value(move[0], alpha, beta, depth-1), key=lambda x: x[0])[0]
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v



def alpha_beta_search(state, depth):
    moves = list(breadth(state))

    _, index = max_value(state, -2147483648, 2147483647, depth)
    return moves[index]



def basic_tree_search(state):
    """performs a very simple 3-ply search. No minimax or anything fancy."""

    moves = list(breadth(state))
    totals = [0] * 28

    for i, player1_move in enumerate(moves):
        # player 1 can win this move
        if evaluate_full(player1_move[0].board, 1) > 500000:
            return player1_move

        total_score = 0
        for player2_move in breadth(player1_move[0]):
            # player 2 will win next move
            if evaluate_full(player2_move[0].board, 1) < -500000:
                totals[i] -= 2147483647
            else:
                for player1_move2 in breadth(player2_move[0]):
                    val = evaluate_full(player1_move2[0].board, 1)
                    total_score += val
        totals[i] += total_score
    return moves[totals.index(max(totals))]

