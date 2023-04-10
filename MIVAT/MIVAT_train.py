from Kuhn import Kuhn, Action, Card
from Opponents.RandomPlayer import RandomPlayer
from Opponents.OptimalPlayer import OptimalPlayer
from Opponents.StrategyPlayer import StrategyPlayer
from MIVAT.MIVAT import MIVAT
import pickle

g = Kuhn(OptimalPlayer(), OptimalPlayer())
est = MIVAT()

number_of_hands = 1000000
for i in range(number_of_hands):
    # Different values of alpha are optimal against random classes of player (non-exploitative)
    g.player1 = OptimalPlayer(i / number_of_hands)
    (payoff, terminal_history) = g.play_round()
    est.observe_training_point(payoff, terminal_history)

print(est.train())
with open("6D_eq_eq_mivat_theta", "wb") as f:
    pickle.dump(est.theta, f)


print(f"Winrate in $/hand of player 1: {(g.player1_value) / number_of_hands}")
print("Optimal winrate for player 1: ", -1/18)