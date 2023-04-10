"""
file: RandomPlayer.py

This file defines a random player for the game of Kuhn Poker, who simply chooses a legal action
at random at each stage of play.
"""

from Kuhn import Card, Action
import random

class RandomPlayer:
    card: Card = -1

    def give_card(self, card: Card):
        self.card = card
    
    def play(self, history: list(Action)):
        if len(history) == 0:
            # For Player 1 there is no history, and must Bet or Check
            return random.choice([Action.Bet, Action.Check])
        elif len(history) == 1:
            if history[0] is Action.Bet:
                # Player 2 must call or fold
                return random.choice([Action.Call, Action.Fold])
            else:
                return random.choice([Action.Bet, Action.Check])
        else:
            return random.choice([Action.Call, Action.Fold])