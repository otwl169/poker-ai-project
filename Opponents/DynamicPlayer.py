### Plays a random strategy for the first 100 hands, then switches to a fully exploitative strategy for player 1
### The true best response requires DynamicPlayer to be given player 1's strategy

from Kuhn import Card, Action
from LinearProgram import Solver
import random

class DynamicPlayer:
    def __init__(self):
        self.card: Card = 0

        # Random and computed strategies
        self.strategy = 0
        self.random_strategy = {'B': {'K': {'B': 0.5, 'P': 0.5},
                                      'Q': {'B': 0.5, 'P': 0.5},
                                      'J': {'B': 0.5, 'P': 0.5}},
                                'P': {'K': {'B': 0.5, 'P': 0.5},
                                      'Q': {'B': 0.5, 'P': 0.5},
                                      'J': {'B': 0.5, 'P': 0.5}}}
        self.best_response = 0

        # Opponent strategy given to DynamicPlayer
        self.opponent_strategy = 0

        # Round number
        self.t = 0

        # Map from Card -> str
        self.card_text = {Card.K: 'K', Card.Q: 'Q', Card.J: 'J'}

        # Linear program solver
        self.s = Solver()

        # Interval to calculate best response
        self.interval = 50

    def give_card(self, card: Card):
        self.card = card

    def play_strategy(self, history: list(Action)):
        if history[0] == Action.Bet:
            bet_chance = self.strategy['B'][self.card_text[self.card]]['B']
            return Action.Call if random.random() < bet_chance else Action.Fold
        else:
            bet_chance = self.strategy['P'][self.card_text[self.card]]['B']
            return Action.Bet if random.random() < bet_chance else Action.Check


    def play(self, history: list(Action)):
        ### Play a round of betting as a dynamic player

        # Player 2 only has 1 round of betting
        self.t += 1

        if self.t <= 100:
            self.strategy = self.random_strategy
        else:
            if self.t % self.interval == 1:
                self.best_response = self.s.get_player2_best_response(self.opponent_strategy)
        
            self.strategy = self.best_response
    
        return self.play_strategy(history)
            
    
    def give_strategy(self, p1_strategy):
        self.opponent_strategy = p1_strategy

