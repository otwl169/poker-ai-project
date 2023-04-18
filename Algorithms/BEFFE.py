from Kuhn import Kuhn, Card, Action

from Modelling.Observed_Model import Model
from LinearProgram import Solver
from Opponents.OptimalPlayer import OptimalPlayer
from Opponents.StrategyPlayer import StrategyPlayer

import random

class BEFFE_Player:

    def __init__(self, T):
        # Value of the game to player i
        self.v = -1/18

        # Gift strategy total k
        self.k = 0

        # Opponent Model
        self.M = Model()

        # LP solver
        self.s = Solver()

        # Current card held
        self.card: Card = -1

        # T = total iterations, t = current iteration
        self.T = T
        self.t = 0

        # Strategy at time step t
        self.strategy = 0

        # Translate cards to strings
        self.card_text = {Card.K: "K", Card.Q: "Q", Card.J: "J"}
    
    def give_card(self, card: Card):
        self.card = card
    
    def detect_gift_strategy(self, terminal_history: list(), payoff):
        # The gift strategies for player 2 in Kuhn poker are:

        if terminal_history[1:4] == [Action.Bet, Card.J, Action.Call]:
            # Calling a bet with a J
            return payoff
        elif terminal_history[1:4] == [Action.Bet, Card.K, Action.Fold]:
            # Folding to a bet with a K
            return payoff
        elif terminal_history[1:4] == [Action.Check, Card.K, Action.Check]:
            # Checking a K if player 1 checks
            return payoff
        elif terminal_history[1:4] == [Action.Check, Card.Q, Action.Bet]:
            # Betting a Q if player 1 checks
            return payoff
        else:
            return 0
    
    def update_internals(self, terminal_history: list(), payoff):
        ### Update the opponent model and gift strategy value k

        # Update opponent model with terminal history 
        # [P1 card, P1 action, P2 card, P2 action, P1 action]
        self.M.observe_action(terminal_history[1], terminal_history[2], terminal_history[3])

        # Update gift strategy value k. If opponent plays a gift strategy we can gain value
        next_k = self.s.get_player1_exploitability(self.strategy) - self.v
        next_k += self.detect_gift_strategy(terminal_history, payoff)
    
    def play_strategy(self, history: list(Action)):
        ### Play according to a behavioural strategy
        if history == []:
            # Round 1 strategy
            bet_chance = self.strategy[1][self.card_text[self.card]]['B']
            return Action.Bet if random.random() < bet_chance else Action.Check
        else:
            # Round 2 strategy
            bet_chance = self.strategy[2][self.card_text[self.card]]['B']
            return Action.Call if random.random() < bet_chance else Action.Fold

    def play(self, history: list(Action)):
        ### Play a round of betting according to BEFFE algorithm

        # Calculate opponent model, best response and exploitability of best response
        opponent_strategy = self.M.calculate_strategy()
        best_response = self.s.get_player1_best_response(opponent_strategy)
        exploitability = self.v - self.s.get_player1_exploitability(best_response)

        # Since we take n_prior equilibrium hands, need to be careful of immediate attempt to exploit
        if self.k >= (self.T - self.t + 1)(self.v - exploitability):
            self.strategy = best_response
        else:
            # Pick best equilibrium strategy
            self.strategy = self.s.get_player1_epsilon_best_response(opponent_strategy, 0)
        
        return self.play_strategy(history)