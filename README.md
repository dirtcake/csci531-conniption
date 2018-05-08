Cris Cummins, Ethan Luckett, Joey Malouf  
  
Win percentages against a random AI  
Going first: 100%  
Going second: 100%  
  
Project overview  
  
Description:  
-Our AI scores a board state based on every group of 4 contiguous spaces.   
-We use a minimax search with alpha beta pruning to find the next best move. We were able to run the program quickly in 6 ply, 
and slowly (90 seconds on turing) at 7 ply. Anything more than that takes too long.  

Board Representation:  
-Board class that holds varaibles for: who's turn it is, p1 flips remaining, p2 flips remaining, 
a boolean to determine if the board was flipped at the end of last turn, and a list of lists filled with 
0's,1's, and 2's that represents the board.  
-Board class also has methods for printing the board, flipping the board, and placing a piece.  

Search:  
-Our AI uses a minimax search and implements alpha beta pruning. The average branching factor of conniption is 21, 
we found that our search cuts that to about 10.5, near optimal for alpha beta pruning  

Expansion:  
-Expands the enxt possible board states depending on the current one.  
-Doesn't have to expand on flip place or flip place flip if the board was flipped at the end of the previous turn.  

Evaluation Function:  
-We assigned a value to every 81 combinations of a 4 by 1 space. For example 1111, has a value of 1,000,000 because 
it's a win, while 0120 has a value of 0 because neither player seems to have an advantage. 2222 would have a value 
of -1,000,000.  
-The scores are opposite if the AI goes second.  
-We later added another array to store different values when looking at 1 wide 4 tall space.  
-We then looked at every possible 4 by 1, horitzontal, diagonal, and vertical splace on the board, summing the score.  

Who worked on what:  

Cris:    
-Created the board representation  
-Wrote the board state class  
-Created a UI  

Ethan:  
-Wrote the evaluation function  
-Wrote the search function (minimax and alpha beta pruning)  
-Rewrote the evaluation function in C to increase speed  
-Wrote the script to play the game  
-Edited every file at least once to fix bugs or add needed code  

Joey:  
-Wrote the expansion function.  
-Debugged sections of code. (Editing board state representation to better fit the expansion/search, making the search 
choose the shortest path to a victory instead of toying with its opponent)  
-Experimented with different values for the evaluation array locally, making the AI worse every time, and never pushing the changes.  

All:  
-Discussed ideas for how everything should work. Board state, expansion, search, evaluation, etc  
