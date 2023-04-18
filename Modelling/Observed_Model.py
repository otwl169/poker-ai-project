# Modified DBBR that looks at observed information

class Model:
    def __init__(self):
        # Player 2 has 2 public history sets, with option of b (add money to pot)
        # or p (add no money)
        self.frequencies = {'B': {'K': {'B': 0, 'P': 0},
                                  'Q': {'B': 0, 'P': 0},
                                  'J': {'B': 0, 'P': 0}},
                            'P': {'K': {'B': 0, 'P': 0},
                                  'Q': {'B': 0, 'P': 0},
                                  'J': {'B': 0, 'P': 0}}}
        
        self.opponent_model = {'B': {'K': {'B': 0, 'P': 0},
                                     'Q': {'B': 0, 'P': 0},
                                     'J': {'B': 0, 'P': 0}},
                               'P': {'K': {'B': 0, 'P': 0},
                                     'Q': {'B': 0, 'P': 0},
                                     'J': {'B': 0, 'P': 0}}}
        
        self.eq_strategy = {'B': {'K': {'B': 1, 'P': 0},
                                  'Q': {'B': 1/3, 'P': 2/3},
                                  'J': {'B': 0, 'P': 1}},
                            'P': {'K': {'B': 1, 'P': 0},
                                  'Q': {'B': 0, 'P': 1},
                                  'J': {'B': 1/3, 'P': 2/3}}}
        
        self.n_prior = 5


    def observe_action(self, p1_action, card, p2_action):
        # Actions must be 'B' or 'P'. Card must be text form ie 'K'
        self.frequencies[p1_action][card][p2_action] += 1
    
    def calculate_strategy(self):
        # uses n_prior fictitious hands played at equilibrium
        # n_prior * eq prob + action count
        for ph_set in self.frequencies:
            for card in self.frequencies[ph_set]:
                bets = self.frequencies[ph_set][card]['B']
                passes = self.frequencies[ph_set][card]['P']

                eq_prob = self.eq_strategy[ph_set][card]['B']
                bet_chance = ((eq_prob * self.n_prior) + bets) / (self.n_prior + bets + passes)

                self.opponent_model[ph_set][card]['B'] = bet_chance
                self.opponent_model[ph_set][card]['P'] = 1 - bet_chance
        
        return self.opponent_model


    