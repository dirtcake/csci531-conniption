
class Evaluator:
    def __init__(self):
        self.lines = {
            # 1 with zero pieces
            (0, 0, 0, 0): 0,
           
            # 8 with one piece
            (0, 0, 0, 1):  1, (0, 0, 1, 0):  1, (0, 1, 0, 0):  1, (1, 0, 0, 0):  1,
            (0, 0, 0, 2): -1, (0, 0, 2, 0): -1, (0, 2, 0, 0): -1, (2, 0, 0, 0): -1,

            # 24 with two pieces
            (0, 0, 1, 1):  16, (0, 1, 0, 1):  16, (0, 1, 1, 0):  16, (1, 0, 0, 1):  16, (1, 0, 1, 0):  16, (1, 1, 0, 0): 16,
            (0, 0, 1, 2):   0, (0, 1, 0, 2):   0, (0, 1, 2, 0):   0, (1, 0, 0, 2):   0, (1, 0, 2, 0):   0, (1, 2, 0, 0):  0,
            (0, 0, 2, 1):   0, (0, 2, 0, 1):   0, (0, 2, 1, 0):   0, (2, 0, 0, 1):   0, (2, 0, 1, 0):   0, (2, 1, 0, 0):  0,
            (0, 0, 2, 2): -16, (0, 2, 0, 2): -16, (0, 2, 2, 0): -16, (2, 0, 0, 2): -16, (2, 0, 2, 0): -16, (2, 2, 0, 0):  -16,

            # 32 with three pieces
            (0, 1, 1, 1):  256, (1, 0, 1, 1):  256, (1, 1, 0, 1):  256, (1, 1, 1, 0):  256,
            (0, 1, 1, 2):    8, (1, 0, 1, 2):    8, (1, 1, 0, 2):    8, (1, 1, 2, 0):    8,
            (0, 1, 2, 1):    4, (1, 0, 2, 1):    4, (1, 2, 0, 1):    4, (1, 2, 1, 0):    4,
            (0, 1, 2, 2):   -8, (1, 0, 2, 2):   -8, (1, 2, 0, 2):   -8, (1, 2, 2 ,0):   -8,
            (0, 2, 1, 1):    8, (2, 0, 1, 1):    8, (2, 1, 0, 1):    8, (2, 1 ,1 ,0):    8,
            (0, 2, 1, 2):   -4, (2, 0, 1 ,2):   -4, (2, 1, 0, 2):   -4, (2, 1, 2, 0):   -4,
            (0, 2 ,2, 1):   -8, (2, 0, 2, 1):   -8, (2, 2, 0, 1):   -8, (2, 2, 1, 0):   -8,
            (0, 2, 2, 2): -256, (2, 0, 2 ,2): -256, (2, 2, 0 ,2): -256, (2, 2, 2, 0): -256,

            # 16 with four pieces
            (1, 1, 1, 1): 1000000,
            (1, 1, 1, 2):  128, (1, 1, 2, 1):  128, (1, 2, 1, 1):  128, (2, 1, 1, 1):  128,
            (1, 1, 2, 2):    0, (1, 2, 1, 2):    0, (1, 2, 2, 1):    0, (2, 1, 1, 2):    0, (2, 1, 2, 1): 0, (2, 2, 1, 1): 0,
            (1, 2, 2, 2): -128, (2, 1, 2, 2): -128, (2, 2, 1, 2): -128, (2, 2, 2, 1): -128,
            (2, 2, 2, 2): -1000000
            }


    def eval_line(self, line):
        '''evaluates a single line of 4 pieces'''
        return self.lines[line]


    def evaluate_full(self, board, player):
        '''evaluates a board state for a specific player.'''

        # for each piece, check the 3 pieces in the column above, in the row to the right, in the up-right diagonal, and
        # in the down-right diagonal
        total = 0
        for c in range(7):
            for r in range(6):
                # check column
                if r < 3:
                    total += self.eval_line(tuple(board[c][r:r+4]))
                
                # check row
                if c < 4:
                    total += self.eval_line(tuple([board[c+i][r] for i in range(4)]))

                # check up-right diagonal
                if r < 3 and c < 4:
                    total += self.eval_line(tuple([board[c+i][r+i] for i in range(4)]))

                # check down-right diagonal
                if r > 2 and c < 4:
                    total += self.eval_line(tuple([board[c+i][r-i] for i in range(4)]))

        if player == 2:
            total = -total
        return total
