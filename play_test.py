#!/usr/bin/env python
from board_class import BoardState
from expand import breadth
from search import basic_tree_search, alpha_beta_search
from evaluate import Evaluator
import time
import sys

def print_board(board):
    for r in range(6):
        for c in range(7):
            piece = board[c][5-r]
            if piece == 0:
                print('.', end=' ')
            else:
                print(piece, end=' ')
        print()
    print('------------')
    print('0 1 2 3 4 5 6\n')


def human_move(state):
    print_board(state.board)
    move = input('enter move: ')
    
    if move.startswith('f'):
        move = move[1:]
        if state.flipped:
            print('You cannot flip the board right now.')
        else:
            state.flip_board()

    state.place_piece(int(move[0]), 2)
    state.player_turn = state.player_turn % 2 + 1

    if move.endswith('f'):
        state.flip_board()
    
    print_board(state.board)


if __name__ == '__main__':
    board = [[0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0]]

    state = BoardState(board, 1, 4, 4)
    ev = Evaluator()


    if '-humanfirst' in sys.argv:
        human_move(state)

    while True:
        print('I am thinking...')
        #state, ai_move = basic_tree_search(state)
        state, ai_move = alpha_beta_search(state, 4)

        if ev.evaluate_full(state.board, 1) >= 500000:
            print_board(state.board)
            print('I win.')
            break

        print('AI move: {}'.format(ai_move))
        human_move(state)

        if ev.evaluate_full(state.board, 1) <= -500000:
            print('You win.')
            break

