from Kuhn import Card, Action
import random


class StrategyPlayer:
    card: Card = -1

    def __init__(self, strategy, player=1):
        self.strategy = strategy
        self.player = player
        self.card_text = {Card.K: 'K', Card.Q: 'Q', Card.J: 'J'}
    
    def give_card(self, card: Card):
        self.card = card
    
    def play(self, history: list(Action)):
        if self.player == 1:
            if history == []:
                bet_chance = self.strategy[1][self.card_text[self.card]]['B']
                return Action.Bet if random.random() < bet_chance else Action.Check
            else:
                bet_chance = self.strategy[2][self.card_text[self.card]]['B']
                return Action.Call if random.random() < bet_chance else Action.Fold
        
        if self.player == 2:
            if history[0] == Action.Bet:
                bet_chance = self.strategy['B'][self.card_text[self.card]]['B']
                return Action.Call if random.random() < bet_chance else Action.Fold
            else:
                bet_chance = self.strategy['P'][self.card_text[self.card]]['B']
                return Action.Bet if random.random() < bet_chance else Action.Check