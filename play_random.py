#!/usr/bin/env python
from play_test import random_move, play
from search import alpha_beta_search
import time
import random
import functools
import sys


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: {} <number of games>'.format(sys.argv[0]))
        sys.exit(0)

    num_games = int(sys.argv[1])
    minimax = functools.partial(alpha_beta_search, depth=3)
    
    wins = {1: 0, 2: 0}
    for i in range(1, num_games+1):
        print('Playing games... {}/{}'.format(i, num_games), end='\r')
        wins[play(random_move, minimax)] += 1
    
    print('\nRandom first: AI won {}%'.format(wins[2] * 100 / num_games))

    wins = {1: 0, 2: 0}
    for i in range(1, num_games+1):
        print('Playing games... {}/{}'.format(i, num_games), end='\r')
        wins[play(minimax, random_move)] += 1

    print('\nAI first: AI won {}%'.format(wins[1] * 100 / num_games))
