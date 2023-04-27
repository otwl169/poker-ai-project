from Kuhn import Card, Action

from Modelling.Observed_Model import Model
from LinearProgram import Solver

import random

class BR_Player:

    def __init__(self):
        # Value of the game to player i
        self.v = -1/18

        # Gift strategy total k
        self.k = 0

        # Opponent Model
        self.M = Model()

        # Current card held
        self.card: Card = -1

        # LP solver
        self.s = Solver()

        # t and interval
        self.t = 0
        self.interval = 50

        # Best response strategy
        self.strategy = 0
        self.exploit = True

        # Translate cards to strings
        self.card_text = {Card.K: "K", Card.Q: "Q", Card.J: "J"}
    
    def give_card(self, card: Card):
        self.card = card
    
    def update_internals(self, terminal_history: list(), payoff):
        # Terminal history:  Card 1 -> P1 -> Card 2 -> P2 -> P1

        # Update opponent model
        p1_action = terminal_history[1].value
        p2_card = self.card_text[terminal_history[2]]
        p2_action = terminal_history[3].value
        self.M.observe_action(p1_action, p2_card, p2_action)

        # Update k
        self.k += 1

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
        # Calculate opponent model 
        
        if history == []:
            # Only update the strategy at the start of the turn
            if self.t % self.interval == 0:
                opponent_strategy = self.M.calculate_strategy()
                self.strategy = self.s.get_player1_best_response(opponent_strategy)
        
        
        return self.play_strategy(history)

        
