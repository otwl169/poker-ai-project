### Plays a random strategy for the first 100 hands, then switches to a fully exploitative strategy for player 1
### The true best response requires DynamicPlayer to be given player 1's strategy

from Kuhn import Card, Action
from LinearProgram import Solver
import random

class DynamicPlayer:
    def __init__(self):
        self.card: Card = 0

        # Random and computed strategies
        self.random_strategy = {'B': {'K': {'B': 0.5, 'P': 0.5},
                                      'Q': {'B': 0.5, 'P': 0.5},
                                      'J': {'B': 0.5, 'P': 0.5}},
                                'P': {'K': {'B': 0.5, 'P': 0.5},
                                      'Q': {'B': 0.5, 'P': 0.5},
                                      'J': {'B': 0.5, 'P': 0.5}}}
        self.best_response = 0

        # Round number
        self.t = 0

        # Map from Card -> str
        self.card_text = {Card.K: 'K', Card.Q: 'Q', Card.J: 'J'}

        # Linear program solver
        self.s = Solver()

    def give_card(self, card: Card):
        self.card = card

    def play(self, history: list(Action)):
        self.t += 1

        if self.t <= 100:
            strategy = self.random_strategy
        else:
            strategy = self.best_response
        
        if history[0] == Action.Bet:
            bet_chance = strategy['B'][self.card_text[self.card]]['B']
            return Action.Call if random.random() < bet_chance else Action.Fold
        else:
            bet_chance = strategy['P'][self.card_text[self.card]]['B']
            return Action.Bet if random.random() < bet_chance else Action.Check
        
        
    def give_strategy(self, p1_strategy):
        self.best_response = self.s.get_player2_best_response(p1_strategy)

