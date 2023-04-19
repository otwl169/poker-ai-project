# Plays within 0.2 of equilibrium strategy. Bets more than it should (+0.2 bet chance at each infoset where there is <0.8 chance to bet)

### adds a uniform random between 0.2 and -0.2 to each action at information set

from Kuhn import Card, Action
import random


class SophisticatedPlayer:
    card: Card = -1

    def __init__(self):
        self.strategy = {'B': {'K': {'B': 1, 'P': 0}, 
                               'Q': {'B': 1/3, 'P': 2/3}, 
                               'J': {'B': 0, 'P': 1}}, 
                         'P': {'K': {'B': 1, 'P': 0}, 
                               'Q': {'B': 0, 'P': 1}, 
                               'J': {'B': 1/3, 'P': 2/3}}}
        self.offset = 0.2
        self.card_text = {Card.K: 'K', Card.Q: 'Q', Card.J: 'J'}
    
    def give_card(self, card: Card):
        self.card = card
    
    def play(self, history: list(Action)):
        # Deviation from equilibrium strategy is within [-0.2. 0.2]
        deviation = (random.random() - 0.5) / (0.5/0.2)
        if history[0] == Action.Bet:
            bet_chance = self.strategy['B'][self.card_text[self.card]]['B']
            return Action.Call if (random.random() + deviation) < bet_chance else Action.Fold
        else:
            bet_chance = self.strategy['P'][self.card_text[self.card]]['B']
            return Action.Bet if (random.random() + deviation) < bet_chance else Action.Check