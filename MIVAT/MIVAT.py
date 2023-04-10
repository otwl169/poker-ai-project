# Learning a value analysis tool for agent evaluation
from Kuhn import Card, Action
import numpy as np

# Denote how chance acts in Kuhn Poker as:

# Chance for P1 Card -> P1 Action 1 -> Chance for P2 Card -> P2 Action -> P1 Action 2



class MIVAT:

    def __init__(self, theta=np.zeros((6,))):
        self.theta = theta

        # Pairs (Payoff, History)
        self.training_data = []

        # List (utility)
        self.money = []

        # List (Est)
        self.trials = []
    
    def phi_2D(self, history: list()):
        # Map histories following a chance node to a vector of 2 features.
        
        # Kuhn Poker is a simple game: 2 Features: (Card Value, Probability of hand winning) multiplied by pot size
        # From point of view of player 1.
        phi = np.zeros((2,))

        if len(history) == 1:
            # P1 Card
            hs = 0
            win_prob = 0
            pot_size = 2

            if history[0] == Card.K:
                hs = 3
                win_prob = 1
            elif history[0] == Card.Q:
                hs = 2
                win_prob = 1/2
            elif history[0] == Card.J:
                hs = 1
                win_prob = 0
            else:
                assert 0
            
            phi[0] = hs
            phi[1] = win_prob
            phi *= pot_size

        elif len(history) >= 3:
            # P1 Card -> P1 Action -> P2 Card
            hs = 0
            win_prob = 0
            pot_size = 2

            if history[1] == Action.Bet:
                pot_size += 1

            hs = history[0].value
            win_prob = (history[0] > history[2])

            phi[0] = hs
            phi[1] = win_prob
            phi *= pot_size
        
        return phi
    
    def phi(self, history: list()):
        # Map histories following a chance node to a vector of 6 features

        # (Hand Strength, Hand Strength squared, Pot equity, HS * HS2, HS * PE, HS2 * PE ) * Pot size
        # Pot equity = Hand Strength when opponent card not yet known

        phi = np.zeros((6,))
        pot_size = 2

        if len(history) == 1:
            if history[0] == Card.K:
                hs = 1   
            elif history[0] == Card.Q:
                hs = 1/2
            elif history[0] == Card.J:
                hs = 0
            
            phi[0] = hs
            phi[1] = hs**2
            phi[2] = hs
        elif len(history) >= 3:
            # Card -> P1 > Card -> P2 -> P1
            if history[2] == Card.K:
                hs = 1
            elif history[2] == Card.Q:
                hs = 1/2
            elif history[2] == Card.J:
                hs = 0
            
            phi[0] = hs
            phi[1] = hs**2
            phi[2] = history[0] > history[2]

        phi[3] = phi[0] * phi[1]
        phi[4] = phi[0] * phi[2]
        phi[5] = phi[1] * phi[2]

        phi *= pot_size
        return phi

    def A_t(self, terminal_history):
        # Terminal history of the form:
        # P1 Card -> P1 Action -> P2 Card -> P2 Action (-> P1 Action)
        all_cards = {Card.K, Card.Q, Card.J}

        # Get phi value of first card draw
        first_draw = self.phi([terminal_history[0]])

        for card in all_cards:
            first_draw -= ((1/3) * self.phi([card]))

        # Get luck value of second card draw
        second_draw = self.phi(terminal_history[0:2])

        for card in (all_cards - {terminal_history[0]}):
            second_draw -= ((1/2) * self.phi([*terminal_history[0:1], card]))
        
        return first_draw + second_draw
    
    def observe_training_point(self, payoff, terminal_history):
        self.training_data.append((payoff, terminal_history))

    def train(self):
        # Use accumulated training data to calculate theta
        
        # Get value of A, u_bar
        A = np.zeros((6,))
        u_bar = 0
        for (payoff, history) in self.training_data:
            u_bar += payoff
            A += self.A_t(history)
        
        A = A / len(self.training_data)
        u_bar = u_bar / len(self.training_data)

        # Get the value of the first part of the theta j equation
        first_part = 0
        for (_, history) in self.training_data:
            a_t = self.A_t(history)
            first_part += a_t @ a_t.T
        
        first_part = first_part / len(self.training_data)
        first_part -= (A @ A.T)

        # Get the value of the second part of the theta j equation
        second_part = np.zeros((6,))
        for (payoff, history) in self.training_data:
            a_t = self.A_t(history)
            second_part += payoff * a_t
        
        second_part = second_part / len(self.training_data)
        second_part -= u_bar * A


        self.theta = second_part / first_part

        return self.theta

    def pred(self, payoff, terminal_history):
        a_t = self.A_t(terminal_history)
        return payoff - (a_t @ self.theta)
    
    def observe_trial(self, payoff, terminal_history):
        estimate = self.pred(payoff, terminal_history)
        self.trials.append(estimate)
        self.money.append(payoff)
    
    def get_average_estimate(self):
        return np.average(self.trials)
    
    def get_money_stdev(self):
        return np.std(self.money)

    def get_estimator_stdev(self):
        return np.std(self.trials)
