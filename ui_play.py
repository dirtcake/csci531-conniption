from tkinter import *
from tkinter import ttk
from time import sleep

root = Tk()
root.title("Play Conniption")


def human_input(*args):  #needs to be renamed, is acutally human piece entry
	place = Tk()
	place.title("Play Conniption")
	game = ttk.Frame(place, padding= "4 4 12 12")
	game.grid(column=0, row=0, stick=(N, W, E, S))
	game.columnconfigure(0, weight=1)
	game.rowconfigure(0, weight=1)

	column_get = IntVar()
	status = StringVar()
	flipping= IntVar()

	ttk.Label(game, text = "Column").grid(column = 1, row = 1, sticky = (W,E))
	column_entry = ttk.Entry(game, width = 7, textvariable = column_get).grid(column = 2, row = 1, sticky =(W,E))
	flipped = ttk.Checkbutton(game, variable= flipping, onvalue = 1, offvalue = 0, text = "Flip").grid(column=3, row =1, sticky= (W, E))
	ttk.Label(game, text = "Status:").grid(column = 1, row = 2, stick =(W))
	ttk.Label(game, textvariable = status). grid(column= 2, row=2, sticky = (W))
	ttk.Button(game, text = "Place Piece", command = play).grid(column = 4, row= 4, sticky=(W)) #does not have the correct fuction call

def ai_output(*args):
	place = Tk()
	place.title("Play Conniption")
	game = ttk.Frame(place, padding= "4 4 12 12")
	game.grid(column=0, row=0, stick=(N,W,E,S))
	game.columnconfigure(0, weight=1)
	game.rowconfigure(0, weight=1)


	status = StringVar()
	games_number = IntVar()
	ttk.Label(game, text= "Number of Games:").grid(column = 1, row = 1, sticky=(W))
	number_of_games = ttk.Entry(game, width=7, textvariable=games_number).grid(column = 2, row=1, sticky=(W))
	ttk.Label(game, text = "Status:").grid(column=1, row=2, sticky=(W))
	ttk.Label(game, textvariable = status).grid(column=2, row=2, sticky=(W))
	ttk.Button(game, text = "Exit", command=ai_output). grid(column=4, row=4, sticky = (E)) #does not have the correct function call


def play(*args): #will fill with player
	if player_type1.get() == "human" or player_type2.get == "human":
		human_input()
	else:
		ai_output()

mainframe = ttk.Frame(root, padding= "4 5 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

player_type1 = StringVar()
player_type2 = StringVar()


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

root.mainloop()