from Kuhn import Kuhn, Card, Action

from Modelling.DBBR import Model
from LinearProgram import *
from Opponents.OptimalPlayer import OptimalPlayer
from Opponents.StrategyPlayer import StrategyPlayer

import random

class BEFEWP_Player:

    def __init__(self, T):
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
    
    def give_card(self, card: Card):
        self.card = card
    
    def update_internals(self, terminal_history: list(), payoff):
        # Terminal history:  Card 1 -> P1 -> Card 2 -> P2 -> P1

        # Update k
        current_strategy = self.br_s.strategy if (self.exploit) else self.eq_s.strategy
        nemesis_ev = get_player1_exploitability(current_strategy)

        # Check if nemesis ever plays this action. If not, add its payoff to k
        nemesis = get_player2_best_response(current_strategy)
        ph_set = 1 if terminal_history[1] == Action.Bet else 2
        nemesis_plays_action = nemesis[ph_set][self.card_match[terminal_history[2]]][terminal_history[3].value]

        if nemesis_plays_action == 0:
            nemesis_ev = nemesis_ev + payoff
    
        self.k = self.k + (nemesis_ev - self.v)

        # IDEA -> u(strat, nemesis that played this move)
        # = value against nemesis (+ value gained from move if nemesis never plays it, and is therefore suboptimal)

        # Increment t
        self.t += 1

        # Check if we should swap to full exploitation yet
        best_response = get_player1_best_response(self.M.opponent_model)
        epsilon = self.v - get_player1_exploitability(best_response)

        if epsilon <= self.k:
            # Then play a best response
            self.br_s.strategy = best_response
            self.exploit = True
        else:
            # Play equilibrium strategy
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

        