from Kuhn import Kuhn, Action, Card
from Opponents.RandomPlayer import RandomPlayer
from Opponents.OptimalPlayer import OptimalPlayer
from Opponents.StrategyPlayer import StrategyPlayer
from MIVAT.MIVAT import MIVAT
import pickle

with open("6D_eq_eq_mivat_theta", "rb") as f:
    theta = pickle.load(f)

g = Kuhn(OptimalPlayer(), OptimalPlayer())
est = MIVAT(theta)

number_of_hands = 100000
for i in range(number_of_hands):
    # Different values of alpha are optimal against random classes of player (non-exploitative)
    g.player1 = OptimalPlayer(i / number_of_hands)
    (payoff, terminal_history) = g.play_round()
    est.observe_trial(payoff, terminal_history)

print(f"Winrate in $/hand of player 1: {(g.player1_value) / number_of_hands}")
print(f"MIVAT estimated winrate: {est.get_average_estimate()}")
print(f"Stdev Money: {est.get_money_stdev()}, Stdev Est: {est.get_estimator_stdev()}")
print("Optimal winrate for player 1: ", -1/18)