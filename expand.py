from board_class import BoardState
from copy import deepcopy


def breadth(board_state):
    flipped_board = flip(deepcopy(board_state.board))
    for i in range(7):
        for j in range(6):
            if board_state.board[i][j] == 0:
                board_state.board[i][j] = board_state.player_turn
                yield(board_state.print_board())
                board_state.board[i][j] = 0
                if j < 6 and not board_state.flipped:
                    for k in range(j, 0, -1):
                        board_state.board[i][k] = board_state.board[i][k-1]
                    board_state.board[i][0] = board_state.player_turn
                    yield(board_state.print_board())
                    for k in range(j):
                        board_state.board[i][k] = board_state.board[i][k+1]
                    board_state.board[i][j] = 0
                break
    for i in range(7):
        for j in range(6):
            if flipped_board[i][j] == 0:
                if not board_state.flipped:
                    flipped_board[i][j] = board_state.player_turn
                    yield(BoardState(flipped_board).print_board())
                    flipped_board[i][j] = 0
                if j < 6:
                    for k in range(j, 0, -1):
                        flipped_board[i][k] = flipped_board[i][k-1]
                    flipped_board[i][0] = board_state.player_turn
                    yield(BoardState(flipped_board).print_board())
                    for k in range(j):
                        flipped_board[i][k] = flipped_board[i][k+1]
                    flipped_board[i][j] = 0
                break


def flip(board):
        for i in board:
            temp_col = []
            for j in i:
                if j != 0:
                    temp_col.append(j)
            temp_col.reverse()
            for j in range(len(temp_col)):
                if i[j] != 0:
                    i[j] = temp_col[j]
        return board

