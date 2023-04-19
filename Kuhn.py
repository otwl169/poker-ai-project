# Kuhn Poker implementation
from enum import IntEnum, Enum
import random
import numpy as np
from Modelling.DBBR import DBBR_Model
from Modelling.Observed_Model import Model

class Card(IntEnum):
    K = 3
    Q = 2
    J = 1

class Action(Enum):
    Bet = "B"
    Check = "P"
    Call = "B"
    Fold = "P"

class Kuhn:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.player1_value = 0
        self.possible_deals = [[Card.K, Card.Q], 
                               [Card.K, Card.J],
                               [Card.Q, Card.K],
                               [Card.Q, Card.J],
                               [Card.J, Card.K],
                               [Card.J, Card.Q]]
        self.card_text = {Card.K: 'K', Card.Q: 'Q', Card.J: 'J'}
        self.t = 0
        # random.seed(10)

    def deal_cards(self):
        # Uniformly deal cards to each player
        cards = random.sample(list(Card), 2)

        self.player1.give_card(cards[0])
        self.player2.give_card(cards[1])
        return cards

    def play_round(self):
        # Play one round of Kuhn poker
        self.t += 1
        cards = self.deal_cards()

        # Specifically for dynamic opponent, give player 1 exact strategy
        # self.player2.give_strategy(self.player1.strategy)
    
        # Get actions of both players
        action1: Action = self.player1.play([])
        action2: Action = self.player2.play([action1])
        history: list(Action) = [action1, action2]

        # Ensure action sets are legal
        assert action1 in self.get_legal_moves([])
        assert action2 in self.get_legal_moves([action1])
        
        # If player 1 must make another action
        action3 = 0
        if self.get_legal_moves([action1, action2]):
            action3: Action = self.player1.play([action1, action2])
            history.append(action3)
        
        # Get payoff of terminal history
        payoff = self.get_history_outcome(history, cards)
        self.player1_value += payoff

        # Add chance actions to terminal history
        terminal_history = [cards[0], action1, cards[1], action2]
        if action3 != 0: terminal_history.append(action3)

        # Update BEFFE / BEFEWP internals with terminal history and payoff
        self.player1.update_internals(terminal_history, payoff)
        
        return (payoff, terminal_history)
    
    def get_legal_moves(self, history: list(Action)):
        if history == []:
            # Player 1 can bet or check
            return [Action.Bet, Action.Check]
        elif history == [Action.Bet]:
            # Player 2 can bet (call) or fold
            return [Action.Call, Action.Fold]
        elif history == [Action.Check]:
            # Player 2 can bet or check
            return [Action.Bet, Action.Check]
        elif history == [Action.Check, Action.Bet]:
            # Player 1 can bet (call) or fold
            return [Action.Call, Action.Fold]
        else:
            return []
    
    def get_pure_strategies(self, player = 1):
        all_strategies = []
        card_strategies = []

        if player == 1:
            # Get card strategy for each round of betting
            for first_round_action in [Action.Bet, Action.Check]:
                if first_round_action == Action.Bet:
                    card_strategies.append({1: "B", 2: "O"})
                else:
                    for second_round_action in self.get_legal_moves([Action.Check, Action.Bet]):
                        card_strategies.append({1: "P", 2: second_round_action.value})
            
        elif player == 2:
            # Get card strategy for each player 1 action
            check_actions = self.get_legal_moves([Action.Check])
            bet_actions = self.get_legal_moves([Action.Bet])
            
            for action1 in check_actions:
                for action2 in bet_actions:
                    card_strategies.append({1: action1.value, 2: action2.value})

        # Get every permutation of strategy for each card
        for K_strat in card_strategies:
            for Q_strat in card_strategies:
                for J_strat in card_strategies:
                    # 27 combinations of strategy for player 1. 64 for player 2.
                    all_strategies.append(K_strat[1] + Q_strat[1] + J_strat[1] + "," +
                                          K_strat[2] + Q_strat[2] + J_strat[2])

        return all_strategies
    
    def get_outcome(self, terminal_history: str, cards: list(Card)):
        # Gets outcome for player 1 where terminal_history is given as a pure strategy

        if terminal_history == "BB":
            # Bet / Call
            return 2 if cards[0] > cards[1] else -2
        elif terminal_history == "BP":
            # Bet / Fold
            return 1
        elif terminal_history == "PP":
            # Check / Check
            return 1 if cards[0] > cards[1] else -1
        elif terminal_history == "PBP":
            # Check / Bet / Fold
            return -1
        elif terminal_history == "PBB":
            # Check / Bet / Call
            return 2 if cards[0] > cards[1] else -2
        else:
            print("Error, not a valid history: " + terminal_history)
    
    def get_history_outcome(self, terminal_history: list(Action), cards: list(Card)):
        if terminal_history == [Action.Bet, Action.Call]:
            return 2 if cards[0] > cards[1] else -2
        elif terminal_history == [Action.Bet, Action.Fold]:
            return 1
        elif terminal_history == [Action.Check, Action.Check]:
            return 1 if cards[0] > cards[1] else -1
        elif terminal_history == [Action.Check, Action.Bet, Action.Fold]:
            return -1
        elif terminal_history == [Action.Check, Action.Bet, Action.Call]:
            return 2 if cards[0] > cards[1] else -2
        else:
            # print("Error, not a valid history: ")
            # print(terminal_history)
            return 0
        
    def get_payoff(self, player1_pure_strategy: str, player2_pure_strategy: str):
        # Payoff calculated from the perspective of player 1 (player 2 is the corresponding negative value)
        # For each card combination, play out the game and store the payoff for each
        total_payoff = 0

        for [player1_card, player2_card] in self.possible_deals:
            # Get payoff for this set of cards

            # Get player 1 first round action
            player1_action = player1_pure_strategy[3 - player1_card.value]

            # Get player 2 response
            player2_action_index_offset = 4 if player1_action == "B" else 0
            player2_action = player2_pure_strategy[player2_action_index_offset + (3 - player2_card.value)]

            # If needed, get player 1 2nd round action
            terminal_history = player1_action + player2_action
            if terminal_history == "PB":
                player1_second_action = player1_pure_strategy[7 - player1_card.value]
                terminal_history += player1_second_action

            # Increment total payoff
            # print(f"{player1_card, player2_card}, {terminal_history}: {self.get_outcome(terminal_history, [player1_card, player2_card])}")
            total_payoff += self.get_outcome(terminal_history, [player1_card, player2_card])
        
        return total_payoff

    def get_payoff_matrix(self):
        player1_strategies = self.get_pure_strategies(1)
        player2_strategies = self.get_pure_strategies(2)

        M = np.zeros((len(player1_strategies), len(player2_strategies)), dtype=int)

        for i, s1 in enumerate(player1_strategies):
            for j, s2 in enumerate(player2_strategies):
                M[i][j] = self.get_payoff(s1, s2)
        
        return M

    def get_behavioural_strategies(self, player = 1):
        strategies = []

        for card in [Card.K, Card.Q, Card.J]:
            if player == 1:
                # These are the 2 actions for the empty public history
                strategies.append([card, Action.Bet])
                strategies.append([card, Action.Check])

                # These are the 2 actions for the strategy where player 1 has to call or fold a bet from
                # player 2
                strategies.append([card, Action.Check, Action.Bet, Action.Call])
                strategies.append([card, Action.Check, Action.Bet, Action.Fold])
            else:
                strategies.append([card, Action.Bet, Action.Call])
                strategies.append([card, Action.Bet, Action.Fold])

                strategies.append([card, Action.Check, Action.Bet])
                strategies.append([card, Action.Check, Action.Check])
        
        return strategies
    
    def get_infoset_strategies_matrix(self, player = 1):
        assert player == 1 or player == 2

        if player == 1:
            # Player 1 has 6 infosets
            infosets = [[Card.K],
                        [Card.K, Action.Check, Action.Bet],
                        [Card.Q],
                        [Card.Q, Action.Check, Action.Bet],
                        [Card.J],
                        [Card.J, Action.Check, Action.Bet]]
            
            # For each of those infosets, player 1 can perform 2 actions
            # in their strategy with some probability
            strategies = self.get_behavioural_strategies(1)
        else:
            # Player 2 has 6 infosets
            infosets = [[Card.K, Action.Bet],
                        [Card.K, Action.Check],
                        [Card.Q, Action.Bet],
                        [Card.Q, Action.Check],
                        [Card.J, Action.Bet],
                        [Card.J, Action.Check]]
            
            # With each of these infosets, player 2 can perform 2 actions
            strategies = self.get_behavioural_strategies(2)

        M = np.zeros((7, 13))
        M[0][0] = 1 # Dummy row
        for i, info in enumerate(infosets):
            for j, s in enumerate(strategies):
                if len(info) == player:
                    # Card only infoset adds -1 to dummy column
                    M[i+1][0] = -1
                
                if s == info[:-1]:
                    # Strategy contained in history of infoset -> must have been played
                    M[i+1][j+1] = -1
                elif s[:-1] == info:
                    # Strategy == Infoset + action
                    M[i+1][j+1] = 1
        
                
                # strategy is infoset + action

                # infoset requires strategy to haave been played -> K, Check, Bet requires to have checked with a K 
        return M
            
    def get_behavioural_strategy_payoff_matrix(self):
        player1_actions = self.get_behavioural_strategies(1)
        player2_actions = self.get_behavioural_strategies(2)

        # Sparse matrix M, with payoffs wherever these actions form a legal terminal history
        M = np.zeros((13, 13))

        for i, a1 in enumerate(player1_actions):
            for j, a2 in enumerate(player2_actions):
                if a1[0] == a2[0]:
                    # If player1 and player 2 have the same cards
                    pass
                elif len(a1) > len(a2):
                    # Final round
                    if a1[1:-1] == a2[1:]:
                        # Agree with history
                        M[i+1][j+1] = self.get_history_outcome(a1[1:], [a1[0], a2[0]])
                elif len(a2) > len(a1):
                    # Bet / Check + Call/fold
                    if a2[1:-1] == a1[1:]:
                        # Agree on history
                        M[i+1][j+1] = self.get_history_outcome(a2[1:], [a1[0], a2[0]])

        return M
    
    def get_strategy_sequences(self, player=1):
        # Get the sequence form strategies for each player
        sequences = []

        # Player 1 sequences are labelled a through l
        if player == 1:
            # Player 1 has 6 infosets - ordered by (ROUND, CARD ascending)
            sequences = [[Card.J, Action.Check],
                         [Card.J, Action.Bet],
                         [Card.Q, Action.Check],
                         [Card.Q, Action.Bet],
                         [Card.K, Action.Check],
                         [Card.K, Action.Bet],

                         [Card.J, Action.Check, Action.Bet, Action.Fold],
                         [Card.J, Action.Check, Action.Bet, Action.Call],
                         [Card.Q, Action.Check, Action.Bet, Action.Fold],
                         [Card.Q, Action.Check, Action.Bet, Action.Call],
                         [Card.K, Action.Check, Action.Bet, Action.Fold],
                         [Card.K, Action.Check, Action.Bet, Action.Call]]

        # Player 2 sequences are labelled m through x
        else:
            # Player 2 has 6 infosets - ordered by (CARD Q, CARD K, CARD J, Pass infoset, Bet infoset)
            sequences = [[Card.Q, Action.Check, Action.Check],
                         [Card.Q, Action.Check, Action.Bet],
                         [Card.Q, Action.Bet, Action.Fold],
                         [Card.Q, Action.Bet, Action.Call],

                         [Card.K, Action.Check, Action.Check],
                         [Card.K, Action.Check, Action.Bet],
                         [Card.K, Action.Bet, Action.Fold],
                         [Card.K, Action.Bet, Action.Call],

                         [Card.J, Action.Check, Action.Check],
                         [Card.J, Action.Check, Action.Bet],
                         [Card.J, Action.Bet, Action.Fold],
                         [Card.J, Action.Bet, Action.Call]]
        
        return sequences
    
    def get_sequences_legal_matrix(self, player=1):
        assert player == 1 or player == 2

        if player == 1:
            # Ordered by (ROUND, CARD ascending)
            infosets = [[Card.J],
                        [Card.Q],
                        [Card.K],
                        [Card.J, Action.Check, Action.Bet],
                        [Card.Q, Action.Check, Action.Bet],
                        [Card.K, Action.Check, Action.Bet]]
            
            sequences = self.get_strategy_sequences(1)
        
        if player == 2:
            # Ordered by ...
            infosets = [[Card.Q, Action.Check],
                        [Card.Q, Action.Bet],
                        [Card.K, Action.Check],
                        [Card.K, Action.Bet],
                        [Card.J, Action.Check],
                        [Card.J, Action.Bet]]
            
            sequences = self.get_strategy_sequences(2)
        

        M = np.zeros((7,13))
        M[0][0] = 1 # Dummy row
        for i, info in enumerate(infosets): 
            for j, seq in enumerate(sequences):          
                if len(info) == player:
                    # Card only infoset adds -1 to dummy column
                    M[i+1][0] = -1
                
                if seq == info[:-1]:
                    # Strategy contained in history of infoset -> must have been played
                    M[i+1][j+1] = -1
                elif seq[:-1] == info:
                    # Strategy == Infoset + action
                    M[i+1][j+1] = 1
            
        return M
        
    
    def get_sequence_payoff_matrix(self):
        # Get each player's sequences
        p1_sequences = self.get_strategy_sequences(1)
        p2_sequences = self.get_strategy_sequences(2)

        # Sparse matrix M, with payoffs wherever these actions form a legal terminal history
        M = np.zeros((13, 13))

        for i, s1 in enumerate(p1_sequences):
            for j, s2 in enumerate(p2_sequences):
                # Make sure that they don't have the same card
                if s1[0] == s2[0]:
                    pass
                elif len(s1) == 2:
                    # Round 1
                    # Ensure that histories agree
                    if s1[1] == s2[1]:
                        # Evaluation of Check + Bet or any other non terminal history will return 0 from history outcome
                        M[i+1][j+1] = self.get_history_outcome(s2[1:], [s1[0], s2[0]])
                
                elif len(s1) == 4:
                    # Round 2
                    # Ensure that histories agree
                    if s1[1:-1] == s2[1:] == [Action.Check, Action.Bet]:
                        M[i+1][j+1] = self.get_history_outcome(s1[1:], [s1[0], s2[0]])
        
        return M / 6


if __name__ == "__main__":
    g = Kuhn(0, 0)
    print(g.get_strategy_sequences(1))
    # print(g.get_strategy_sequences(2))