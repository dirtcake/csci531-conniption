class BoardState:

 def __init__(self, board):
 	
 	if board == NULL:
 		board_create()
 	else:
 		self.board = board
 	self.flipped = False

 def board_create(self):
 	self.board = []
 	for i in range(7):
 		temp_col = []
 		self.board.append(temp_col)


 def place_piece(self, pos, player):
 	placed = False
 	if len(self.board[pos]) < 6:
 		self.board[pos].append(player)
 		self.flipped = False
 		placed = True
 	return placed


 def print_board(self):
 	print(self.board)

 def flip_board(self):
 	for i in range(7):
 		self.board[i].reverse()
 	self.flipped = True