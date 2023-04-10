# DBBR algorithm from "Game Theory-Based Opponent Modeling in Large Imperfect-Information Games" 2011 Sandholm
from Kuhn import *



# Player 2 will have the public history sets:
# [Bet], [Check]
# This has the possible actions:
# [Call, Fold], [Check, Bet]


# DBBR:
# In practice, computing a full model for the opponent and a best response might be too slow - this
# can be mitigated by computing such an exploitative strategy every k iterations

# Compute posterior action probabilities:
# This involves:
# 1) Assuming that the opponent plays their actions according their observed frequency
# 2) Mixing in this assumption with a precomputed equilibrium strategy that then allows the model to cope with informations sets which
#    have 0 actions played so far

# Computing posterior bucket probabilities:
# The probablity that the opponent is at each bucket in n, given our model of his play so far
# This involves:
# 1) BFS traversal of public history sets
# 2) 

class Model:
    # Model for player 2 strategy
    def __init__(self):
        # Player 2 has 2 public history sets, with option of b (add money to pot)
        # or p (add no money)
        self.ph_frequencies = {'B': {'B': 0, 'P': 0},
                               'P': {'B': 0, 'P': 0}}
        
        self.ph_probabilities = {'B': {'B': 0, 'P': 0},
                                 'P': {'B': 0, 'P': 0}}

        # [Public_history][Private_info][Action] = probability
        self.equilibrium_model = {'B': {'K': {'B': 1, 'P': 0}, 
                                        'Q': {'B': 1/3, 'P': 2/3},
                                        'J': {'B': 0, 'P': 1}},

                                  'P': {'K': {'B': 1, 'P': 0},
                                        'Q': {'B': 0, 'P': 1},
                                        'J': {'B': 1/3, 'P': 2/3}}}

        self.equilibrium_probabilities = {'B': {'B': 4/9, 'P': 5/9},
                                          'P': {'B': 4/9, 'P': 5/9}}

        self.n_prior = 5

        # Probability opponent is in each bucket at each public history set
        # Bucket corresponds to cards held ie. private information
        # [Public_history][Bucket]
        self.bucket_probabilities = {'B': {'K': 0, 
                                           'Q': 0,
                                           'J': 0},

                                     'P': {'K': 0,
                                           'Q': 0,
                                           'J': 0}}

        # Opponent strategy initialised to equilibrium strategy
        self.opponent_model = {'B': {'K': {'B': 1, 'P': 0}, 
                                     'Q': {'B': 1/3, 'P': 2/3},
                                     'J': {'B': 0, 'P': 1}},

                               'P': {'K': {'B': 1, 'P': 0},
                                     'Q': {'B': 0, 'P': 1},
                                     'J': {'B': 1/3, 'P': 2/3}}}
        
        self.ws_probs = self.ph_probabilities
        self.bet_probability_ordering = {'B': ['K', 'Q', 'J'], 
                                         'P': ['K', 'J', 'Q']}

    

    def observe_action(self, history, action):
        self.ph_frequencies[history][action] += 1
    
    def compute_posterior_action_probabilities(self):
        # Probability opponent makes action at each public history set

        for ph_set in self.ph_frequencies:
            total_actions = sum(self.ph_frequencies[ph_set].values())

            for action in self.ph_frequencies[ph_set]:
                self.ph_probabilities[ph_set][action] = ( self.equilibrium_probabilities[ph_set][action] * self.n_prior + self.ph_frequencies[ph_set][action] ) / ( self.n_prior + total_actions )

    def compute_bucket_probabilities(self):
        # In Kuhn Poker, since player 2 has only one action round, and no compound actions:
        # The probability that he is in bucket b at ph set n is simply 1/3, for each card draw

        for ph_set in self.bucket_probabilities:
            for private_info in self.bucket_probabilities[ph_set]:
                self.bucket_probabilities[ph_set][private_info] = 1/3

        # Can maybe change this to use the info from player 1's strategy to analyse which bucket player 2 can be in
        # e.g. if player 1 always bets with a king, player 2 can never call / fold a king
    
    def update_ws_probs(self):
        # Update weight shifting probabilities to match the changes made to self.opponent_model
        for ph_set in self.opponent_model:
            b_chance = 0
            for private_info in self.opponent_model[ph_set]:
                b_chance += self.opponent_model[ph_set][private_info]['B'] / 3
            
            self.ws_probs[ph_set]['B'] = b_chance
            self.ws_probs[ph_set]['P'] = 1 - b_chance
    
    def compute_full_opponent_strategy(self):
        # Using custom weight shifting algorithm from DBBR paper

        self.opponent_model = self.equilibrium_model
        self.ws_probs = self.equilibrium_probabilities
    
        # Sort all buckets by how often the equilibrium strategy bets with them

        # Check whether opponent is betting more often than equilibrium

        # If opponent bets more:
        # Add weight to the bucket that bets most in equilibrium strategy

        for ph_set in self.ph_probabilities:
            if self.ph_probabilities[ph_set]['B'] > self.ws_probs[ph_set]['B']:
                # If the opponent bets more than the equilibrium

                for card in self.bet_probability_ordering[ph_set]:
                    # Get the cards in order of how often they are bet with by the equilibrium strategy

                    if self.ws_probs[ph_set]['B'] + (self.bucket_probabilities[ph_set][card] * (1 - self.opponent_model[ph_set][card]['B'])) < self.ph_probabilities[ph_set]['B']:
                        # The probability that opponent model bets + (chance in this bucket * (1- prob opponent model bets with this bucket) < observed bet frequency at this ph set
                        # If we were to set the chance of betting with this bucket in opponent model to 1, the observed frequency is higher
                        delta = 1 - self.opponent_model[ph_set][card]['B']
                        self.opponent_model[ph_set][card]['B'] = 1
                        self.opponent_model[ph_set][card]['P'] = 0
                    else:
                        # We cannot set this probability to 1, so update accordingly
                        
                        delta = (self.ph_probabilities[ph_set]['B'] - self.ws_probs[ph_set]['B']) / self.bucket_probabilities[ph_set][card]

                        self.opponent_model[ph_set][card]['B'] += delta
                        self.opponent_model[ph_set][card]['P'] -= delta

                    new_action_prob = self.ws_probs[ph_set]['B'] + delta * self.bucket_probabilities[ph_set][card]
                    self.ws_probs[ph_set]['B'] = new_action_prob
                    self.ws_probs[ph_set]['P'] = 1 - new_action_prob

                    if self.ws_probs[ph_set]['B'] + (self.bucket_probabilities[ph_set][card] * (1 - self.opponent_model[ph_set][card]['B'])) > self.ph_probabilities[ph_set]['B']:
                        break

    def model_opponent(self):
        self.compute_posterior_action_probabilities()
        self.compute_bucket_probabilities()
        self.compute_full_opponent_strategy()
        return self.opponent_model
