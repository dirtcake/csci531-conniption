#!/usr/bin/env python
from board_class import BoardState
from expand import breadth
from search import alpha_beta_search
from cevaluate.evaluate import evaluate_full
#from evaluate import Evaluator
import functools
import random
import sys


#eval = Evaluator()

def human_move(state):
    print('P1 flips:', state.p1_flips)
    print('P2 flips:', state.p2_flips)
    move = input('Enter move: ')

    if state.player_turn == 1:
        flips = state.p1_flips
    else:
        flips = state.p2_flips

    if move.startswith('f') and flips > 0:
        move = move[1:]
        if state.flipped:
            print('You cannot flip the board right now.')
        else:
            state.flip_board()
            if state.player_turn == 1:
                state.p1_flips -= 1
            else:
                state.p2_flips -= 1

    state.place_piece(int(move[0]), state.player_turn)

    if move.endswith('f') and flips > 0:
        state.flip_board()
        if state.player_turn == 1:
            state.p1_flips -= 1
        else:
            state.p2_flips -= 1

    state.player_turn = state.player_turn % 2 + 1

    return state, [0, 0]


def random_move(state):
    moves = list(breadth(state))
    return random.choice(moves)


def play(player1, player2):
    state = BoardState()

    if player1 == human_move or player2 == human_move:
        state.print_board()

    while True:
        state, move = player1(state)

        if player1 == human_move or player2 == human_move:
            state.print_board()

        # if eval.evaluate_full(state.board, 1) >= 500000:
        if evaluate_full(state.board, 1) >= 500000:
            return 1

        state, move = player2(state)

        if player1 == human_move or player2 == human_move:
            state.print_board()

        # if eval.evaluate_full(state.board, 2) >= 500000:
        if evaluate_full(state.board, 2) >= 500000:
            return 2


def usage():
    print('Usage: {} <player1> <player2>'.format(sys.argv[0]))
    print('Valid players: human, random, minimax')


if __name__ == '__main__':
    agents = {
            'random': random_move,
            'human': human_move,
            'minimax': functools.partial(alpha_beta_search, depth=6),
    }

    if len(sys.argv) < 3 or sys.argv[1] not in agents or sys.argv[2] not in agents:
        usage()
        sys.exit(0)

    player1 = agents[sys.argv[1]]
    player2 = agents[sys.argv[2]]

    result = play(player1, player2)
    print('Player {} ({}) wins.'.format(result, sys.argv[result]))

