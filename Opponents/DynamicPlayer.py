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

        self.best_response_eq = {'B': {'K': {'B': 1, 'P': 0}, 
                                       'Q': {'B': 1/3, 'P': 2/3}, 
                                       'J': {'B': 0, 'P': 1}}, 
                                 'P': {'K': {'B': 1, 'P': 0}, 
                                       'Q': {'B': 0, 'P': 1}, 
                                       'J': {'B': 1/3, 'P': 2/3}}}
        self.best_response_br = 0

        # Opponent strategy given to DynamicPlayer, store both the equilibrium strategy and the 
        # best response strategy
        self.opponent_eq_strategy = 0
        self.opponent_br_strategy = 0

        # Set to true when the opponent chooses to play a best response
        self.opponent_exploiting = False

        # Round number
        self.t = 0

        # Map from Card -> str
        self.card_text = {Card.K: 'K', Card.Q: 'Q', Card.J: 'J'}

        # Linear program solver
        self.s = Solver()

        # Interval to calculate best response
        self.interval = 50

        self.modify_strategy()

    def give_card(self, card: Card):
        self.card = card

    def modify_strategy(self):
        # Choose strategy at each information set uniformly at random
        for ph_set in self.random_strategy:
            for infoset in self.random_strategy[ph_set]:
                bet_chance = random.random()
                self.random_strategy[ph_set][infoset]['B'] = bet_chance

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
                # Calculates its own best response to new calculation from opponent directly after they calculate their strategy
                if self.opponent_br_strategy != 0:
                    self.best_response_br = self.s.get_player2_best_response(self.opponent_br_strategy)

            if self.opponent_exploiting:
                if self.best_response_br == 0:
                    self.best_response_br = self.s.get_player2_best_response(self.opponent_br_strategy)
                self.strategy = self.best_response_br
            else:
                self.strategy = self.best_response_eq
    
        return self.play_strategy(history)
            
    
    def give_strategy(self, p1_strategy, p1_exploit):
        if p1_exploit:
            self.opponent_br_strategy = p1_strategy
            self.opponent_exploiting = True
        else:
            self.opponent_eq_strategy = p1_strategy
            self.opponent_exploiting = False
            

