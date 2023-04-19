from Kuhn import *

# Import algorithms
from Algorithms.BEFFE import BEFFE_Player

# Import opponent classes
from Opponents.OptimalPlayer import OptimalPlayer
from Opponents.RandomPlayer import RandomPlayer
from Opponents.StrategyPlayer import StrategyPlayer
from Opponents.SophisticatedPlayer import SophisticatedPlayer

# Import OS to check if file exists
import os.path
import time

RESULTS_FILE = "Results/BEFFE_sophisticated_10k"
number_of_tests = 10_000
number_of_hands = 1000

assert not os.path.exists(RESULTS_FILE)

# Open text file to write results to
t1 = time.time()
with open(RESULTS_FILE, "a") as fh:
    buffer = []
    for i in range(number_of_tests):
        # Play against opponent for 1000 hands

        g = Kuhn(BEFFE_Player(1000), SophisticatedPlayer())
        for _ in range(number_of_hands):
            (payoff, terminal_history) = g.play_round()
        
        buffer.append(g.player1_value / 1000)
        if len(buffer) >= 1000:
            # Write to file
            fh.write('\n'.join(map(str, buffer)) + '\n')
            tn = time.time()
            print(f"Test {i+1} completed in {tn-t1} time")
            buffer = []
    
    fh.write('\n'.join(map(str, buffer)) + '\n')

t2 = time.time()
print(f"Finished testing in {t2 - t1} time")