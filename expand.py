from board_class import BoardState
from copy import deepcopy
import time


class Expand:

    def __init__(self, board_state, player, end_flip):
        self.board = deepcopy(board_state.board)
        board_state.flip_board()
        self.flipped_board = deepcopy(board_state.board)
        self.player = player
        self.end_flip = end_flip

    def breadth(self):
        for i in range(7):
            for j in range(6):
                if self.board[i][j] == 0:
                    self.board[i][j] = self.player
                    yield(BoardState(self.board).print_board())
                    self.board[i][j] = 0
                    if j < 6 and not self.end_flip:
                        for k in range(j, 0, -1):
                            self.board[i][k] = self.board[i][k-1]
                        self.board[i][0] = self.player
                        yield(BoardState(self.board).print_board())
                        for k in range(j):
                            self.board[i][k] = self.board[i][k+1]
                        self.board[i][j] = 0
                    break
        for i in range(7):
            for j in range(6):
                if self.flipped_board[i][j] == 0:
                    if not self.end_flip:
                        self.flipped_board[i][j] = self.player
                        yield(BoardState(self.flipped_board).print_board())
                        self.board[i][j] = 0
                    if j < 6:
                        for k in range(j, 0, -1):
                            self.flipped_board[i][k] = self.flipped_board[i][k-1]
                        self.flipped_board[i][0] = self.player
                        yield (BoardState(self.flipped_board).print_board())
                        for k in range(j):
                            self.flipped_board[i][k] = self.flipped_board[i][k+1]
                        self.flipped_board[i][j] = 0
                    break


ahh = BoardState(None)
ahh.place_piece(1, 1)
ahh.place_piece(1, 2)
ahh.place_piece(1, 1)
ahh.place_piece(1, 1)
ahh.place_piece(1, 1)
stuff = Expand(ahh, 1, True)
count = 0
start = time.time()
for board in stuff.breadth():
    count += 1
print(count)
end = time.time()
print(end-start)
