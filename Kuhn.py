# Kuhn Poker implementation
from enum import IntEnum, Enum
import random

class Card(IntEnum):
    K = 3
    Q = 2
    J = 1

class Action(Enum):
    Bet = 1
    Check = 2
    Call = 3
    Fold = 4

class Kuhn:
    def __init__(self, player1, player2):
        self.pot_value = 2
        self.player1 = player1
        self.player2 = player2
        self.player1_value = 0
        self.player2_value = 0

    def reset(self):
        self.pot_value = 2

    def deal_cards(self):
        # Uniformly deal cards to each player
        cards = random.sample(list(Card), 2)

        self.player1.give_card(cards[0])
        self.player2.give_card(cards[1])
        return cards
    
    def reward_highest_card(self, cards: list(Card)):
        # Reward current pot value to the player with the highest card value
        assert len(cards) == 2

        if cards[0] > cards[1]:
            self.player1_value += self.pot_value
        else:
            self.player2_value += self.pot_value

    def play_round(self):
        # Play one round of Kuhn poker
        cards = self.deal_cards()

        # Cost of ante
        self.player1_value -= 1
        self.player2_value -= 1
    
        # Get actions of both players
        action1: Action = self.player1.play([])
        action2: Action = self.player2.play([action1])

        # Ensure action sets are legal
        if action1 == Action.Bet:
            assert action2 in {Action.Call, Action.Fold}
        elif action1 == Action.Check:
            assert action2 in {Action.Bet, Action.Check}
        else:
            assert action1 not in {Action.Call, Action.Fold}
        
        # Reward players accordingly
        if action2 is Action.Fold:
            self.player1_value -= 1 # For betting
            self.pot_value = 3
            self.player1_value += self.pot_value
        elif action2 is Action.Call:
            # Player 1 must have bet, therefore pot value is 4
            self.player1_value -= 1
            self.player2_value -= 1
            self.pot_value = 4
            self.reward_highest_card(cards)
        elif action2 is Action.Check:
            self.reward_highest_card(cards)
        elif action2 is Action.Bet:
            # Cost of bet
            self.player2_value -= 1

            # Get Player 1's response
            action3: Action = self.player1.play([action1, action2])

            # Assert response is valid
            assert action3 in {Action.Call, Action.Fold}

            # Rewards players accordingly
            if action3 is Action.Fold:
                self.pot_value = 3
                self.player2_value += self.pot_value
            else:
                self.player1_value -= 1
                self.pot_value = 4
                self.reward_highest_card(cards)
        else:
            assert False