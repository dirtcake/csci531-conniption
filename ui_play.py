#!/usr/bin/env python
from board_class import BoardState
from expand import breadth
from search import alpha_beta_search
from cevaluate.evaluate import evaluate_full
import functools
import random
import sys
from tkinter import *
from tkinter import ttk

root = Tk()
global player_type1 
global player_type2 
global column_get 
global status  #use this to display if the AI is thinking or if a player has has won
global flipping1
global flipping2 
global flips_get_P1 
global flips_get_P2 
global state

	
def human_move(*args):
	global state
	state.print_board()
	first_move = True
	if player_type1.get() == "minimax" and first_move == False:
		state, move = functools.partial(alpha_beta_search, depth=6)
		if evaluate_full(state.board, 1) >= 500000:
		 	status.set("Player 1 wins")
	
	if state.player_turn == 1:
		flips = state.p1_flips
	else:
		flips = state.p2_flips
	if flipping1.get() and flips > 0:
		if state.flipped:
			status.set('You cannot flip the board right now.')
		else:
			state.flip_board()
			if state.player_turn == 1:
				state.p1_flips -= 1
			else:
				state.p2_flips -= 1

	state.place_piece(column_get.get(), state.player_turn)

	if flipping2.get() and flips > 0:
		state.flip_board()
		if state.player_turn == 1:
			state.p1_flips -= 1
		else:
			state.p2_flips -= 1

	flips_get_P1.set(state.p1_flips)
	flips_get_P2.set(state.p2_flips)
	state.player_turn = state.player_turn % 2 + 1
	first_move = False

	if player_type1.get() == "human":
		 if evaluate_full(state.board, 1) >= 500000:
		 	status.set("Player 1 wins")

	elif player_type2.get() == "human":
		if evaluate_full(state.board, 2) >= 500000:
			status.set("Player 2 wins")

	if player_type2.get() == "minimax":
		state, move = functools.partial(alpha_beta_search, depth=6)
		if evaluate_full(state.board, 2) >= 500000:
			status.set("PLayer 2 wins")
	state.print_board()


	
def human_input(*args):  #needs to be renamed, is acutally human piece entry
	place = Toplevel()
	place.title("Play Conniption")
	game = ttk.Frame(place, padding= "4 4 12 12")
	game.grid(column=0, row=0, sticky=(N, W, E, S))
	game.columnconfigure(0, weight=1)
	game.rowconfigure(0, weight=1)
	flips_get_P1.set(state.p1_flips)
	flips_get_P2.set(state.p2_flips)
	if player_type2.get() == "human":
		status.set("You are Player 2")
	elif player_type1.get() == "human":
		status.set("You are Player 1")


	ttk.Label(game, text = "Column").grid(column = 1, row = 1, sticky = (W,E))
	column_entry = ttk.Entry(game, width = 7, textvariable = column_get).grid(column = 2, row = 1, sticky =(W,E))
	flipped = ttk.Checkbutton(game, variable= flipping1, text = "Flip Before", offvalue = False, onvalue = True).grid(column=3, row =1, sticky= (W, E))
	flipped2 = ttk.Checkbutton(game, variable= flipping2, text = "Flip Before", offvalue = False, onvalue = True).grid(column=4, row =1, sticky= (W, E))
	ttk.Label(game, text = "Status:").grid(column = 1, row = 2, stick =(W))
	ttk.Label(game, textvariable = status).grid(column= 2, row=2, sticky = (W))
	ttk.Label(game, text = "P1 Flips:").grid(column = 1, row=3, sticky = (W,E))
	ttk.Label(game, textvariable = flips_get_P1).grid(column =2, row =3, sticky =(W,E))
	ttk.Label(game, text = "P2 Flips:").grid(column=1, row=4, sticky =(W,E))
	ttk.Label(game, textvariable = flips_get_P2).grid(column =2, row=4, sticky =(W,E))

	ttk.Button(game, text = "Place Piece", command=human_move).grid(column = 5, row= 4, sticky=(W)) #does not have the correct fuction call	

def play(*args): #will fill with player
	if player_type1 == "minimax":
		state, move = functools.partial(alpha_beta_search, depth=6)

	if player_type1.get() == "human" or player_type2.get() == "human":
		human_input()


	

def game_mode(root):

	root.title("Play Conniption")
	mainframe = ttk.Frame(root, padding= "4 5 12 12")
	mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
	mainframe.columnconfigure(0, weight=1)
	mainframe.rowconfigure(0, weight=1)
	ttk.Label(mainframe, text = "Pick Who Plays Which Player").grid(column = 1, row =1, sticky=(W,E))
	ttk.Label(mainframe, text = "Player 1").grid(column=1, row=2, sticky=(W))
	ttk.Label(mainframe, text= "Player 2").grid(column =1, row=3, sticky=(W))
	ttk.Button(mainframe, text="Submit", command=play).grid(column=4, row=4, sticky = W)
	ttk.Radiobutton(mainframe, text= "Human", variable=player_type1, value="human").grid(column=2, row=2, sticky=(E,W))
	ttk.Radiobutton(mainframe, text= "Random", variable=player_type1, value="random").grid(column=3, row=2, sticky=(E,W))
	ttk.Radiobutton(mainframe, text= "AI", variable=player_type1, value="minimax").grid(column=4, row=2, sticky=(W))
	ttk.Radiobutton(mainframe, text= "Human", variable=player_type2, value="human").grid(column=2, row=3, sticky=(E,W))
	ttk.Radiobutton(mainframe, text= "Random", variable=player_type2, value="random").grid(column=3, row=3, sticky=(E,W))
	ttk.Radiobutton(mainframe, text= "AI", variable=player_type2, value="minimax").grid(column=4, row=3, sticky=(W))


state = BoardState()
player_type1 = StringVar()
player_type2 = StringVar()
column_get = IntVar()
status = StringVar() #use this to display if the AI is thinking or if a player has has won
flipping1= BooleanVar()
flipping2 = BooleanVar()
flips_get_P1 = IntVar()
flips_get_P2 = IntVar()
game_mode(root)
root.mainloop()