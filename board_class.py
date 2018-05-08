class BoardState:

    def __init__(self, board=None, turn=1, p1_flips=4, p2_flips=4, flipped=False):

        if board is None:
            self.board_create()
        else:
            self.board = board
        self.flipped = flipped
        self.player_turn = turn
        self.p1_flips = p1_flips
        self.p2_flips = p2_flips

    def board_create(self):
        self.board = []
        for i in range(7):
            self.board.append([0, 0, 0, 0, 0, 0])

    def place_piece(self, pos, player):
        placed = False
        for i in range(6):
            if self.board[pos][i] == 0:
                self.board[pos][i] = player
                self.flipped = False
                placed = True
                break

        self.flipped = False
        return placed

    def print_board(self):
        for r in range(6):
            for c in range(7):
                piece = self.board[c][5 - r]
                if piece == 0:
                    print('.', end=' ')
                else:
                    print(piece, end=' ')
            print()
        print('------------')
        print("0 1 2 3 4 5 6")

    def flip_board(self):
        for i in self.board:
            temp_col = []
            for j in i:
                if j != 0:
                    temp_col.append(j)
            temp_col.reverse()
            for j in range(len(temp_col)):
                if i[j] != 0:
                    i[j] = temp_col[j]

        self.flipped = True
