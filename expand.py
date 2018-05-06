from board_class import BoardState


def breadth(board_state):
    flipped_board = flip([list(col) for col in board_state.board])
    board = [list(col) for col in board_state.board]

    # know how many flips the current player
    if board_state.player_turn == 1:
        flips = board_state.p1_flips
    else:
        flips = board_state.p2_flips

    for i in [3, 2, 4, 1, 5, 0, 6]:
        for j in range(6):
            # Place with no flips
            if board[i][j] == 0:
                board[i][j] = board_state.player_turn
                yield(BoardState([list(col) for col in board], board_state.player_turn % 2 + 1, board_state.p1_flips,
                                 board_state.p2_flips), [i, j])
                board[i][j] = 0
                break

    if flips > 0:
        if not board_state.flipped:
            for i in [3, 2, 4, 1, 5, 0, 6]:
                for j in range(6):
                    # Flip then place
                    if flipped_board[i][j] == 0:
                        flipped_board[i][j] = board_state.player_turn
                        if board_state.player_turn == 1:
                            yield (BoardState([list(col) for col in flipped_board], board_state.player_turn % 2 + 1,
                                              board_state.p1_flips - 1, board_state.p2_flips, False), [i, j])
                            flipped_board[i][j] = 0
                        if board_state.player_turn == 2:
                            yield (BoardState([list(col) for col in flipped_board], board_state.player_turn % 2 + 1,
                                              board_state.p1_flips, board_state.p2_flips - 1, False), [i, j])
                            flipped_board[i][j] = 0
                        break

        for i in [3, 2, 4, 1, 5, 0, 6]:
            for j in range(6):
                # Place then flip
                if flipped_board[i][j] == 0:
                    for k in range(j, 0, -1):
                        flipped_board[i][k] = flipped_board[i][k-1]
                    flipped_board[i][0] = board_state.player_turn
                    if board_state.player_turn == 1:
                        yield (BoardState([list(col) for col in flipped_board], board_state.player_turn % 2 + 1,
                                          board_state.p1_flips - 1, board_state.p2_flips, True), [i, j])
                    if board_state.player_turn == 2:
                        yield (BoardState([list(col) for col in flipped_board], board_state.player_turn % 2 + 1,
                                          board_state.p1_flips, board_state.p2_flips - 1, True), [i, j])
                    for k in range(j):
                        flipped_board[i][k] = flipped_board[i][k+1]
                    flipped_board[i][j] = 0
                    break

    if flips > 1 and not board_state.flipped:
        for i in [3, 2, 4, 1, 5, 0, 6]:
            for j in range(6):
                # Flip place flip
                if board[i][j] == 0:
                    for k in range(j, 0, -1):
                        board[i][k] = board[i][k-1]
                    board[i][0] = board_state.player_turn
                    if board_state.player_turn == 1:
                        yield (BoardState([list(col) for col in board], board_state.player_turn % 2 + 1, board_state.p1_flips - 2,
                                          board_state.p2_flips, True), [i, j])
                    if board_state.player_turn == 2:
                        yield (BoardState([list(col) for col in board], board_state.player_turn % 2 + 1, board_state.p1_flips,
                                          board_state.p2_flips - 2, True), [i, j])
                    for k in range(j):
                        board[i][k] = board[i][k+1]
                    board[i][j] = 0
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
