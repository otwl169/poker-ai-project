from Kuhn import Card, Action

from Modelling.Observed_Model import Model
from LinearProgram import Solver

import random

class BEFEWP_Player:

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

        # Strategy at time step t, type of strategy at time step t
        self.strategy = 0
        self.exploit = False
        
        # Computed best reponse and best response exploitability
        self.best_response = 0
        self.exploitability = 0

        # Computed best equilibrium strategie
        self.best_equilibrium = 0

        # Translate cards to strings
        self.card_text = {Card.K: "K", Card.Q: "Q", Card.J: "J"}

        # How many rounds to play before calculating strategies
        self.interval = 50
    
    def give_card(self, card: Card):
        self.card = card
    
    def detect_gift_strategy(self, terminal_history: list(), payoff):
        # The gift strategies for player 2 in Kuhn poker are:

        if terminal_history[1:4] == [Action.Bet, Card.J, Action.Call]:
            # Calling a bet with a J has EV to player 1 of 1/3 (4/6-1/6)
            return self.strategy[1]['K']['B']/6 + self.strategy[1]['Q']['B']/6
        elif terminal_history[1:4] == [Action.Bet, Card.K, Action.Fold]:
            # Folding to a bet with a K has EV to player 1 of 1/3 WOULD HAVE (-4/6) BUT HAVE (2/6)
            return self.strategy[1]['Q']['B']*(3/6) + self.strategy[1]['J']['B']*(3/6)
        elif terminal_history[1:4] == [Action.Check, Card.K, Action.Check]:
            # Checking a K if player 1 checks has EV to player 1 of 1/6?????
            q_val = (1-self.strategy[1]['Q']['B'])*self.strategy[2]['Q']['B']/6
            j_val = (1-self.strategy[1]['J']['B'])*self.strategy[2]['J']['B']/6
            return q_val + j_val
        elif terminal_history[1:4] == [Action.Check, Card.Q, Action.Bet]:
            # Betting a Q if player 1 checks has EV 1/6 * 0 + 1/6 * 1 # 0 - (1-2)
            return (1-self.strategy[1]['K']['B'])/6
        else:
            return 0
    
    def update_internals(self, terminal_history: list(), payoff):
        ### Update the opponent model, gift strategy value k and t

        # Update opponent model with terminal history 
        # [P1 card, P1 action, P2 card, P2 action, P1 action]
        p1_action = terminal_history[1].value
        p2_card = self.card_text[terminal_history[2]]
        p2_action = terminal_history[3].value
        self.M.observe_action(p1_action, p2_card, p2_action)

        # Update gift strategy value k. If opponent plays a gift strategy we can gain value
        current_nemesis_ev = self.v if not self.exploit else self.v - self.exploitability
        self.k += current_nemesis_ev + self.detect_gift_strategy(terminal_history, payoff) - self.v

        # Update t
        self.t += 1
    
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
        # Only if t is a multiple of self.interval (every self.interval rounds)
        if history == []:
            # Only update the strategy at the start of the turn
            if self.t % self.interval == 0:
                opponent_strategy = self.M.calculate_strategy()
                self.best_response = self.s.get_player1_best_response(opponent_strategy)
                self.exploitability = self.v - self.s.get_player1_exploitability(self.best_response)
                self.best_equilibrium = self.s.get_player1_epsilon_best_response(opponent_strategy, 0)

            # If nemesis wouldn't expect to take all of our value in remaining turns, attempt to exploit
            if self.exploitability <= self.k:
                self.strategy = self.best_response
                self.exploit = True
            else:
                # Pick best equilibrium strategy
                self.strategy = self.best_equilibrium
                self.exploit = False
        
        return self.play_strategy(history)