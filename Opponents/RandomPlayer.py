"""
file: RandomPlayer.py

This file defines a random player for the game of Kuhn Poker, who simply chooses a legal action
at random at each stage of play.
"""

from Kuhn import Card, Action
import random

class RandomPlayer:
    # Random player 2, actions chosen with static probability chosen uniformly at random at each infoset
    def __init__(self):
        self.random_strategy = {'B': {'K': {'B': 0.5, 'P': 0.5},
                                      'Q': {'B': 0.5, 'P': 0.5},
                                      'J': {'B': 0.5, 'P': 0.5}},
                                'P': {'K': {'B': 0.5, 'P': 0.5},
                                      'Q': {'B': 0.5, 'P': 0.5},
                                      'J': {'B': 0.5, 'P': 0.5}}}
        
        self.card: Card = -1

        # Map from Card -> str
        self.card_text = {Card.K: 'K', Card.Q: 'Q', Card.J: 'J'}

        self.modify_strategy()

    def give_card(self, card: Card):
        self.card = card

    def modify_strategy(self):
        # Choose strategy at each information set uniformly at random
        for ph_set in self.random_strategy:
            for infoset in self.random_strategy[ph_set]:
                bet_chance = random.random()
                self.random_strategy[ph_set][infoset]['B'] = bet_chance
    
    def play(self, history: list(Action)):
        if history[0] == Action.Bet:
            bet_chance = self.random_strategy['B'][self.card_text[self.card]]['B']
            return Action.Call if random.random() < bet_chance else Action.Fold
        else:
            bet_chance = self.random_strategy['P'][self.card_text[self.card]]['B']
            return Action.Bet if random.random() < bet_chance else Action.Check