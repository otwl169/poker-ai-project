from Kuhn import Kuhn
import numpy as np
from scipy.optimize import linprog
import cvxpy as cp

class PureStrategySolver:
    def __init__(self):
        self.g = Kuhn(0, 0)

        # Get normal payoff matrix for Kuhn Poker
        self.P = self.g.get_payoff_matrix()

        # Normalize normal payoff matrix
        self.M = self.P + abs(np.min(self.P))

    ### Minimax theorem based linear program for player 1 optimal strategy
    def get_player1_equilibrium(self):
        # Uses normal form strategies
        # c[0] = v, value of game. c[1:] is mixed strategy for player 1
        c = np.zeros((28,))
        c[0] = -1

        # Assert that sum of probabilities = 1
        A_eq = np.ones((28,))
        A_eq[0] = 0
        b_eq = [1]

        # Using strategy x, achieve at least value of game against any strategy from player 2
        negative_column_constraints = self.M.T * -1
        A_ub = np.vstack([np.ones((64,)), negative_column_constraints.T]).T
        b_ub = np.zeros((64,))

        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=[A_eq], b_eq=b_eq)
        print(res.x)
        print((res.fun * 3))

        print(np.where(res.x[1:] > 0))
        print(self.g.get_pure_strategies(1)[5])
        print(self.g.get_pure_strategies(1)[6])

    ### Minimax theorem based linear program for player 2 optimal strategy
    def get_player2_equilibrium(self):
        # Uses normal form strategies
        # c[0] = v, value of game. c[1:] is the mixed strategy for player 2
        c = np.zeros((65,))
        c[0] = 1

        # Assert that sum of probabilities = 1
        A_eq = np.ones((65,))
        A_eq[0] = 0
        b_eq = [1]

        # Using strategy y, achieve at most the value of the game against any strategy from player 1
        negative_column_constraints = self.M * -1
        A_ub = np.vstack([np.ones(27,), negative_column_constraints.T]).T * -1
        b_ub = np.zeros((27,))

        res2 = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=[A_eq], b_eq=b_eq)
        print(res2.x)

        print(np.where(res2.x[1:] > 0))
        print(self.g.get_pure_strategies(2)[9])
        print(self.g.get_pure_strategies(2)[15])




class Solver:
    ### A solver based on the sequence form of behavioural strategies
    def __init__(self):
        # Game
        self.g = Kuhn(0, 0)

        ### Simplified player 1 and player 2 matrices based on behavioural strategies
        self.P = self.g.get_sequence_payoff_matrix()

        # Get strategy eq matrices
        self.E = self.g.get_sequences_legal_matrix(1)
        self.e = np.zeros(7)
        self.e[0] = 1

        self.F = self.g.get_sequences_legal_matrix(2)
        self.f = np.zeros(7)
        self.f[0] = 1

        # Value of the game (to player 1)
        self.v = -1/18
    
    def get_player1_equilibrium(self):
        x = cp.Variable(13)
        q = cp.Variable(7)

        objective = cp.Maximize((-q.T) @ self.f)
        constraints = [((x.T @ (-self.P)) - (q.T @ self.F)) <= 0]
        constraints.append(x.T @ self.E.T == self.e.T)
        constraints.append(x >= 0)

        problem = cp.Problem(objective, constraints)
        problem.solve()

        return np.round(x.value, 3)

    def get_player2_equilibrium(self):
        y = cp.Variable(13)
        p = cp.Variable(7)

        objective = cp.Minimize((self.e.T) @ p)
        constraints = [(-(self.P @ y) + (self.E.T @ p)) >= 0]
        constraints.append(-self.F @ y == -self.f)
        constraints.append(y >= 0)

        problem = cp.Problem(objective, constraints)
        problem.solve()

        return np.round(y.value, 3)   

    def get_player1_best_response(self, strategy):
        y = self.transform_strategy_to_vector(strategy, 2)
        x = cp.Variable(13)

        objective = cp.Maximize(x @ self.P @ y)
        constraints = [x >= 0]
        constraints.append(x.T @ self.E.T == self.e.T)     

        problem = cp.Problem(objective, constraints)
        problem.solve()

        # Round the strategy sequence and output it as a behavioural dictionary
        br = self.transform_vector_to_strategy(np.round(x.value, 5), 1)
        return br
    
    def get_player1_epsilon_best_response(self, strategy, epsilon=0):
        y = self.transform_strategy_to_vector(strategy, 2)
        x = cp.Variable(13)
        q = cp.Variable(7)

        objective = cp.Maximize(x.T @ self.P @ y)
        constraints = [x.T @ self.E.T == self.e.T]
        constraints.append(x.T @ self.P >= -(q @ self.F))
        constraints.append(q[0] == epsilon - self.v)
        constraints.append(x >= 0)

        problem = cp.Problem(objective, constraints)
        problem.solve()

        # Round the strategy sequence and output it as a behavioural dictionary
        br = self.transform_vector_to_strategy(np.round(x.value, 5), 1)
        return br
    
    def get_player1_best_response_and_exploitability(self, strategy):
        y = self.transform_strategy_to_vector(strategy, 2)
        x = cp.Variable(13)
        q = cp.Variable(7)

        objective = cp.Maximize(x.T @ self.P @ y)
        constraints = [x.T @ self.E.T == self.e.T]
        constraints.append(x.T @ self.P >= -(q @ self.F))
        constraints.append(x >= 0)

        problem = cp.Problem(objective, constraints)
        problem.solve()

        # Round the strategy sequence and output it as a behavioural dictionary
        br = self.transform_vector_to_strategy(np.round(x.value, 5), 1)
        expl = np.round(q.value[0] + self.v, 3)
        return br, expl

    def get_player1_exploitability(self, strategy):
        # Get exploitability by computing the expected value of a nemesis strategy
        x = self.transform_strategy_to_vector(strategy, 1)
        y = cp.Variable(13)

        objective = cp.Minimize(x @ self.P @ y)
        constraints = [y >= 0]
        constraints.append(-self.F @ y == -self.f)

        problem = cp.Problem(objective, constraints)
        problem.solve()

        return problem.value
    
    def get_player2_best_response(self, strategy):
        x = self.transform_strategy_to_vector(strategy, 1)
        y = cp.Variable(13)

        objective = cp.Minimize(x @ self.P @ y)
        constraints = [-self.F @ y == -self.f]
        constraints.append(y >= 0)

        problem = cp.Problem(objective, constraints)
        problem.solve()

        # Round the strategy sequence and output it as a behavioural dictionary
        br = self.transform_vector_to_strategy(np.round(y.value, 5), 2)
        return br 

    def transform_vector_to_strategy(self, vector, player=1):
        # Transform vector output into behavioural strategy

        if player == 1:
            # Sequences a to l ordered by Round then Card ascending then Pass then Bet
            strategy = {1: {'K': {'B': 0, 'P': 0},
                            'Q': {'B': 0, 'P': 0},
                            'J': {'B': 0, 'P': 0}},
                        2: {'K': {'B': 0, 'P': 0},
                            'Q': {'B': 0, 'P': 0},
                            'J': {'B': 0, 'P': 0}}}
            
            for i, card in enumerate(['J', 'Q', 'K']):
                strategy[1][card]['P'] = vector[(2*i)+1]
                strategy[1][card]['B'] = vector[(2*i)+2]

                if strategy[1][card]['P'] > 0:
                    # Only if we have a chance of reaching the second round
                    strategy[2][card]['P'] = vector[(2*i)+7] / strategy[1][card]['P']
                    strategy[2][card]['B'] = vector[(2*i)+8] / strategy[1][card]['P']

        elif player == 2:
            # Sequences m to x ordered by Pass then Bet on Q->K->J
            strategy = {'B': {'K': {'B': 0, 'P': 0},
                              'Q': {'B': 0, 'P': 0},
                              'J': {'B': 0, 'P': 0}},
                        'P': {'K': {'B': 0, 'P': 0},
                              'Q': {'B': 0, 'P': 0},
                              'J': {'B': 0, 'P': 0}}}
            
            for i, card in enumerate(['Q', 'K', 'J']):
                strategy['P'][card]['P'] = vector[(4*i)+1]
                strategy['P'][card]['B'] = vector[(4*i)+2]
                strategy['B'][card]['P'] = vector[(4*i)+3]
                strategy['B'][card]['B'] = vector[(4*i)+4]
        
        return strategy
    
    def transform_strategy_to_vector(self, strategy, player=1):
        vector = np.zeros(13)
        vector[0] = 1

        if player == 1:
            for i, card in enumerate(['J', 'Q', 'K']):
                # These two probabilities implicitly sum to 1
                vector[(2*i)+1] = strategy[1][card]['P']
                vector[(2*i)+2] = strategy[1][card]['B']

                if strategy[1][card]['P'] > 0:
                    # Weight second round probabilities against probability of passing for player 1 in round 1
                    vector[(2*i)+7] = strategy[2][card]['P'] * strategy[1][card]['P']
                    vector[(2*i)+8] = strategy[2][card]['B'] * strategy[1][card]['P']

            assert np.allclose(vector.T @ self.E.T, self.e.T, atol=1e-03)
    
        elif player == 2:
            for i, card in enumerate(['Q', 'K', 'J']):
                # Bet and pass must sum to 1 (which happens implicitly)
                vector[(4*i)+1] = strategy['P'][card]['P']
                vector[(4*i)+2] = strategy['P'][card]['B']
                vector[(4*i)+3] = strategy['B'][card]['P']
                vector[(4*i)+4] = strategy['B'][card]['B']

            assert np.allclose(-self.F @ vector, -self.f, atol=1e-03)
    
        return vector
            


if __name__ == "__main__":
    s = Solver()

    # x = s.get_player1_equilibrium()
    # y = s.get_player2_equilibrium()

    # p1_eq = s.transform_vector_to_strategy(x, 1)
    # print(p1_eq)
    # p1_vec = s.transform_strategy_to_vector(p1_eq, 1)
    # print(p1_vec)
    # print(y)
    # p2_eq = s.transform_vector_to_strategy(y, 2)
    # print(p2_eq)
    # p2_vec = s.transform_strategy_to_vector(p2_eq, 2)
    # print(p2_vec)

    # print(s.get_player1_exploitability(p1_eq))
    random_s = {'B': {'K': {'B': 0.5, 'P': 0.5},
                  'Q': {'B': 0.5, 'P': 0.5},
                  'J': {'B': 0.5, 'P': 0.5}},
            'P': {'K': {'B': 0.5, 'P': 0.5},
                  'Q': {'B': 0.5, 'P': 0.5},
                  'J': {'B': 0.5, 'P': 0.5}}}

    br, expl  = s.get_player1_best_response_and_exploitability(random_s)
    print(br, expl)
    print(s.get_player1_exploitability(br))


    x = np.array([1, 1, 0, 0.44901, 0.55099, 0, 1, 1, 0, 0.2245, 0.2245, 0, 0,])
    l = x.T @ s.E.T
    print(l)


    print(np.allclose(l, s.e.T))
    print(np.allclose(l, s.e.T, atol=1e-03))