class Evaluator:
    def __init__(self):
        self.lines = {
            # 1 with zero pieces
            '0000': 0, 
           
            # 8 with one piece
            '0001':  1, '0010':  1, '0100':  1, '1000':  1,
            '0002': -1, '0020': -1, '0200': -1, '2000': -1,

            # 24 with two pieces
            '0011':  16, '0101':  16, '0110':  16, '1001':  16, '1010':  16, '1100': 16,
            '0012':   0, '0102':   0, '0120':   0, '1002':   0, '1020':   0, '1200':  0,
            '0021':   0, '0201':   0, '0210':   0, '2001':   0, '2010':   0, '2100':  0,
            '0022': -16, '0202': -16, '0220': -16, '2002': -16, '2020': -16, '2200':  -16,

            # 32 with three pieces
            '0111':  256, '1011':  256, '1101':  256, '1110':  256,
            '0112':    8, '1012':    8, '1102':    8, '1120':    8,
            '0121':    4, '1021':    4, '1201':    4, '1210':    4,
            '0122':   -8, '1022':   -8, '1202':   -8, '1220':   -8,
            '0211':    8, '2011':    8, '2101':    8, '2110':    8,
            '0212':   -4, '2012':   -4, '2102':   -4, '2120':   -4,
            '0221':   -8, '2021':   -8, '2201':   -8, '2210':   -8,
            '0222': -256, '2022': -256, '2202': -256, '2220': -256,

            # 16 with four pieces
            '1111': 1000000,
            '1112':  128, '1121':  128, '1211':  128, '2111':  128,
            '1122':    0, '1212':    0, '1221':    0, '2112':    0, '2121':   0, '2211':    0,
            '1222': -128, '2122': -128, '2212': -128, '2221': -128,
            '2222': -1000000
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
                    total += self.eval_line(''.join([board[c][r+i] for i in range(4)]))
                
                # check row
                if c < 4:
                    total += self.eval_line(''.join([board[c+i][r] for i in range(4)]))

                # check up-right diagonal
                if r < 3 and c < 4:
                    total += self.eval_line(''.join([board[c+i][r+i] for i in range(4)]))

                # check down-right diagonal
                if r > 2 and c < 4:
                    total += self.eval_line(''.join([board[c+i][r-i] for i in range(4)]))

        if player == 2:
            total = -total
        return total
