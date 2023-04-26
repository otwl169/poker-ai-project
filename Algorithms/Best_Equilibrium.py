from Kuhn import Kuhn, Card, Action

from Modelling.Observed_Model import Model
from LinearProgram import Solver


import random

class BE_player:

    def __init__(self):
        # Opponent Model
        self.M = Model()

        # LP solver
        self.s = Solver()

        # Current card held
        self.card: Card = -1

        # t is current iteration
        self.t = 0

        # Strategy at time step t
        self.strategy = 0

        # Translate cards to strings
        self.card_text = {Card.K: "K", Card.Q: "Q", Card.J: "J"}

        # How many rounds to play before calculating strategies
        self.interval = 25

        # For integration
        self.exploit = False
    
    def give_card(self, card: Card):
        self.card = card
    
    def update_internals(self, terminal_history: list(), payoff):
        ### Update Opponent model and t

        # Update opponent model with terminal history 
        # [P1 card, P1 action, P2 card, P2 action, P1 action]
        p1_action = terminal_history[1].value
        p2_card = self.card_text[terminal_history[2]]
        p2_action = terminal_history[3].value
        self.M.observe_action(p1_action, p2_card, p2_action)

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
        ### Play a round of betting using the best equilibrium strategy at each point

        # Calculate opponent model, and best equilibrium
        if history == []:
            # Only update the strategy at the start of the turn
            if self.t % self.interval == 0:
                opponent_strategy = self.M.calculate_strategy()
                self.strategy= self.s.get_player1_epsilon_best_response(opponent_strategy, 0)
        
        return self.play_strategy(history)