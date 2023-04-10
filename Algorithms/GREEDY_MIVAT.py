from Kuhn import Kuhn, Card, Action

from Modelling.DBBR import Model
from LinearProgram import *
from Opponents.OptimalPlayer import OptimalPlayer
from Opponents.StrategyPlayer import StrategyPlayer

import random

class GREEDY_MIVAT_Player:

    def __init__(self, T, est):
        # Value of the game to player i
        self.v = -1/18

        # Gift strategy total k
        self.k = 0

        # Opponent Model
        self.M = Model()

        # Current card held
        self.card: Card = -1

        # T = total iterations, t = current iteration
        self.T = T
        self.t = 0

        # Equilibrium strategy
        self.eq_s = OptimalPlayer()

        # Given strategy player
        self.br_s = StrategyPlayer(0)

        # Mode: Exploit or Equilibrium
        self.exploit = False

        # Translate cards to strings
        self.card_match = {Card.K: "K", Card.Q: "Q", Card.J: "J"}

        # MIVAT estimator
        self.est = est
    
    def give_card(self, card: Card):
        self.card = card
    
    def update_internals(self, terminal_history: list(), payoff):
        # Terminal history:  Card 1 -> P1 -> Card 2 -> P2 -> P1

        # Update k
        self.k = self.k + self.est.pred(payoff, terminal_history)

        # Increment t
        self.t += 1

        if self.k > 0:
            self.exploit = True
        else:
            self.exploit = False
    
    def play(self, history: list(Action)):
        # Calculate opponent model 
        opponent_strategy = self.M.model_opponent()

        best_response = get_player1_best_response(opponent_strategy)

        if self.exploit:
            # Then play a best response
            self.br_s.strategy = best_response
            self.br_s.give_card(self.card)
            return self.br_s.play(history)
        else:
            # Play equilibrium strategy
            self.eq_s.give_card(self.card)
            return self.eq_s.play(history)

        
