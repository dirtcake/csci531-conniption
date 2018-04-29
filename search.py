from expand import breadth
from board_class import BoardState
from cevaluate.evaluate import evaluate_full
from copy import deepcopy

def basic_tree_search(state):
    """performs a very simple 3-ply search. No minimax or anything fancy."""

    moves = list(x[0] for x in map(deepcopy, breadth(state)))
    totals = [0] * 28

    for i, player1_move in enumerate(moves):
        # player 1 can win this move
        if evaluate_full(player1_move.board, 1) > 500000:
            return player1_move

        total_score = 0
        for player2_move in (x[0] for x in map(deepcopy, breadth(player1_move))):
            # player 2 will win next move
            if evaluate_full(player2_move.board, 1) < -500000:
                totals[i] -= 2147483647
            else:
                for player1_move2 in (x[0] for x in map(deepcopy, breadth(player2_move))):
                    val = evaluate_full(player1_move2.board, 1)
                    total_score += val
        totals[i] += total_score
    return moves[totals.index(max(totals))]

