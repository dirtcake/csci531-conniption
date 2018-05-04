
class Evaluator:
    def __init__(self):
        self.evals = [
                       0,   1,   -1,   1,      16,    0,   -1,    0,      -16,# 0000-0022
                       1,  16,    0,  16,     256,    8,    0,    4,       -8,# 0100-0122
                      -1,   0,  -16,   0,       8,   -4,  -16,   -8,     -256,# 0200-0222
                       1,  16,    0,  16,     256,    8,    0,    4,       -8,# 1000-1022
                      16, 256,    8, 256, 1000000,  128,    8,  128,        0,# 1100-1122
                       0,   4,   -8,   4,     128,    0,   -8,    0,     -128,# 1200-1222
                      -1,   0,  -16,   0,       8,   -4,  -16,   -8,     -256,# 2000-2022
                       0,   8,   -4,   8,     128,    0,   -4,    0,     -128,# 2100-2122
                     -16,  -8, -256,  -8,       0, -128, -256, -128, -1000000 # 2200-2222
                     ]

    def evaluate_full(self, board, player):
        """evaluates a board state for a specific player."""

        # each line of 4 pieces is treated as a ternary string, converted to decimal, then used as an array index
        # for each piece, check the 3 pieces in the column above, in the row to the right, in the up-right diagonal, and
        # in the down-right diagonal
        total = 0
        winner = 0
        for c in range(7):
            for r in range(6):
                start = board[c][r] * 27

                # check column
                if r < 3:
                    index = start + board[c][r+1] * 9 + board[c][r+2] * 3 + board[c][r+3]
                    if (self.evals[index] > 500000 and player == 1) or (self.evals[index] < -500000 and player == 2):
                        winner = player
                    total += self.evals[index]
                
                if c < 4:
                    # check row
                    index = start + board[c+1][r] * 9 + board[c+2][r] * 3 + board[c+3][r]
                    if (self.evals[index] > 500000 and player == 1) or (self.evals[index] < -500000 and player == 2):
                        winner = player
                    total += self.evals[index]

                    if r < 3:
                        # check up-right diagonal
                        index = start + board[c+1][r+1] * 9 + board[c+2][r+2] * 3 + board[c+3][r+3]
                        if (self.evals[index] > 500000 and player == 1) or (self.evals[index] < -500000 and player == 2):
                            winner = player
                        total += self.evals[index]
                    else:
                        # check down-right diagonal
                        index = start + board[c+1][r-1] * 9 + board[c+2][r-2] * 3 + board[c+3][r-3]
                        if (self.evals[index] > 500000 and player == 1) or (self.evals[index] < -500000 and player == 2):
                            winner = player
                        total += self.evals[index]

        if player == 2:
            total = -total

        if winner == player:
            total = 1000000

        return total

