class BoardState:

 def __init__(self, board):
 	
 	if board == None:
 		board_create()
 	else:
 		self.board = board
 	self.flipped = False

 def board_create(self):
 	self.board = []
 	for i in range(7):
 		self.board.append([0,0,0,0,0,0])


 def place_piece(self, pos, player):
 	placed = False
 	for i in range(6):
 		if self.board[pos][i] == 0:
 			self.board[pos][i] = player
 			placed = True
 			break

 	return placed


 def print_board(self):
 	print(self.board)

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