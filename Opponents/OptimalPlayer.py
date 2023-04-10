"""
file: OptimalPlayer.py

This file defines an optimal player class which will play at some Nash equilibrium for the game
of Kuhn Poker, parameterised on alpha.
"""

from Kuhn import Card, Action
import random

class OptimalPlayer:
    card: Card = -1
    
    def __init__(self, alpha = 1):
        self.alpha = alpha
        self.strategy = {1: {'K': {'B': alpha, 'P': 1 - alpha}, 
                             'Q': {'B': 0, 'P': 1},
                             'J': {'B': alpha/3, 'P': 1-alpha/3}},
                         2: {'K': {'B': 1, 'P': 0}, 
                             'Q': {'B': (alpha+1)/3, 'P': 1-(alpha+1)/3},
                             'J': {'B': 0, 'P': 1}}}
    
    def give_card(self, card: Card):
        self.card = card

    def play(self, history: list(Action)):
        assert len(history) <= 2

        if len(history) == 0:
            # First round strategy: Player 1
            if self.card == Card.J:
                # Bet with probability alpha/3
                return Action.Bet if random.random() < self.alpha/3 else Action.Check
            elif self.card == Card.Q:
                # Always check
                return Action.Check
            else:
                # Bet with probability alpha
                return Action.Bet if random.random() < self.alpha else Action.Check
        
        elif len(history) == 1:
            # Second round strategy: Player 2
            if history == [Action.Bet]:
                if self.card == Card.J:
                    # Always fold
                    return Action.Fold
                elif self.card == Card.Q:
                    # Call with probability 1/3
                    return Action.Call if random.random() < 1/3 else Action.Fold
                else:
                    # Always call
                    return Action.Call
            else:
                if self.card == Card.J:
                    # Bet with probability 1/3
                    return Action.Bet if random.random() < 1/3 else Action.Check
                elif self.card == Card.Q:
                    # Always check
                    return Action.Check
                else:
                    # Always bet
                    return Action.Bet

        else:
            # Third round strategy: Player 1
            if self.card == Card.J:
                # Always fold
                return Action.Fold
            elif self.card == Card.Q:
                # Call with probability alpha/3 + 1/3
                return Action.Call if random.random() < (self.alpha/3 + 1/3) else Action.Fold
            else:
                # Always call
                return Action.Call