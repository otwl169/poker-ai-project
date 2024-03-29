from Kuhn import *

# Player Types
from Opponents.RandomPlayer import RandomPlayer
from Opponents.OptimalPlayer import OptimalPlayer
from Opponents.StrategyPlayer import StrategyPlayer
from Opponents.SophisticatedPlayer import SophisticatedPlayer
from Opponents.DynamicPlayer import DynamicPlayer


from Algorithms.Pure_Best_Response import BR_Player
from Algorithms.BEFFE import BEFFE_Player
from Algorithms.BEFEWP import BEFEWP_Player
from Algorithms.MBEFFE import MBEFFE_Player
from Algorithms.MBEFEWP import MBEFEWP_Player
# from Algorithms.BEFEWP_MIVAT import BEFEWP_MIVAT_Player


from MIVAT.MIVAT import MIVAT
from LinearProgram import *

import pickle

import time

# Set random seed here, and verify that it causes all cards dealt to be the same on each playthrough

# Strategies
test_s = {1: {'K': {'B': 0.501, 'P': 0.499}, 'Q': {'B': 0.0, 'P': 1.0}, 'J': {'B': 1.0, 'P': 0.0}}, 2: {'K': {'B': 1.0, 'P': 0.0}, 'Q': {'B': 0.0, 'P': 1.0}, 'J': {'B': 0, 'P': 0}}}
test_s2 = {1: {'K': {'B': 0.4875, 'P': 0.5125}, 'Q': {'B': 0.0, 'P': 1.0}, 'J': {'B': 1.0, 'P': 0.0}}, 2: {'K': {'B': 1.0, 'P': 0.0}, 'Q': {'B': 0.0, 'P': 1.0}, 'J': {'B': 0, 'P': 0}}}
# Sophisticated player plays within 0.2 of equilibrium
so_s = {1: {'K': {'B': 0.8, 'P': 0.2}, 'Q': {'B': 1/3 + 0.2, 'P': 2/3 - 0.2}, 'J': {'B': 0.2, 'P': 0.8}}, 2: {'K': {'B': 0.8, 'P': 0.2}, 'Q': {'B': 0.2, 'P': 0.8}, 'J': {'B': 1/3 + 0.2, 'P': 2/3 - 0.2}}}



# Load pretrained MIVAT weights
with open("MIVAT/6D_eq_eq_mivat_theta", "rb") as f:
    theta = pickle.load(f)

est = MIVAT(theta)


number_of_hands = 1_000
g = Kuhn(MBEFEWP_Player(1000, est), SophisticatedPlayer())


t1 = time.time()
for i in range(number_of_hands):
    # Different values of alpha are optimal against random classes of player (non-exploitative)
    (payoff, terminal_history) = g.play_round()
    # est.observe_trial(payoff, terminal_history)

t2 = time.time()
print(g.player1.num_mivat_exploits)
print(f"Winrate in $/hand of player 1: {(g.player1_value) / number_of_hands}")
# print(f"Player 2 computed strategy: {g.player2_model.calculate_strategy()}")
# print(f"Estimated winrate using MIVAT: {est.get_average_estimate()}")
print("Value of the game for player 1: ", -1/18)
print(f"Ran in {t2 - t1} seconds")

