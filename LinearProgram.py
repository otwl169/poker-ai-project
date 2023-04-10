from Kuhn import Kuhn
import numpy as np
from scipy.optimize import linprog

g = Kuhn(0, 0)

# Get normal payoff matrix for Kuhn Poker
P = g.get_payoff_matrix()

# Normalize normal payoff matrix
M = P + abs(np.min(P))

### Minimax theorem based linear program for player 1 optimal strategy
def get_player1_equilibrium():
    # Uses normal form strategies
    # c[0] = v, value of game. c[1:] is mixed strategy for player 1
    c = np.zeros((28,))
    c[0] = -1

    # Assert that sum of probabilities = 1
    A_eq = np.ones((28,))
    A_eq[0] = 0
    b_eq = [1]

    # Using strategy x, achieve at least value of game against any strategy from player 2
    negative_column_constraints = M.T * -1
    A_ub = np.vstack([np.ones((64,)), negative_column_constraints.T]).T
    b_ub = np.zeros((64,))

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=[A_eq], b_eq=b_eq)
    print(res.x)

    print(np.where(res.x[1:] > 0))
    print(g.get_pure_strategies(1)[5])
    print(g.get_pure_strategies(1)[6])

### Minimax theorem based linear program for player 2 optimal strategy
def get_player2_equilibrium():
    # Uses normal form strategies
    # c[0] = v, value of game. c[1:] is the mixed strategy for player 2
    c = np.zeros((65,))
    c[0] = 1

    # Assert that sum of probabilities = 1
    A_eq = np.ones((65,))
    A_eq[0] = 0
    b_eq = [1]

    # Using strategy y, achieve at most the value of the game against any strategy from player 1
    negative_column_constraints = M * -1
    A_ub = np.vstack([np.ones(27,), negative_column_constraints.T]).T * -1
    b_ub = np.zeros((27,))

    res2 = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=[A_eq], b_eq=b_eq)
    print(res2.x)

    print(np.where(res2.x[1:] > 0))
    print(g.get_pure_strategies(2)[9])
    print(g.get_pure_strategies(2)[15])

### Calculate a fully exploitative strategy for player 1
def get_exploitative_strategy(player2_strategy):
    assert len(player2_strategy) == 64

### Simplified player 1 and player 2 matrices based on behavioural strategies
M2 = g.get_behavioural_strategy_payoff_matrix()

# Get strategy eq matrices
E = g.get_infoset_strategies_matrix(1)
F = g.get_infoset_strategies_matrix(2)


def transform_strategy_to_vector(strategy, player):
    # Transforms a strategy for player 2 into form needed for LP
    y = np.zeros((13,))
    y[0] = 1

    if player == 1:
        for i, card in enumerate(['K', 'Q', 'J']):
            y[1 + (4*i)] = strategy[1][card]['B']
            y[2 + (4*i)] = strategy[1][card]['P']

            if y[2 + (4*i)] != 0:
                y[3 + (4*i)] = strategy[2][card]['B'] * y[2 + (4*i)]
                y[4 + (4*i)] = strategy[2][card]['P'] * y[2 + (4*i)]

    if player == 2:
        for i, card in enumerate(['K', 'Q', 'J']):
            y[1 + (4*i)] = strategy['B'][card]['B']
            y[2 + (4*i)] = strategy['B'][card]['P']
            y[3 + (4*i)] = strategy['P'][card]['B']
            y[4 + (4*i)] = strategy['P'][card]['P']
    
    return y

def transform_vector_to_strategy(vector, player=1):
    strategy = {1: {'K': {'B': 0, 'P': 0}, 
                    'Q': {'B': 0, 'P': 0},
                    'J': {'B': 0, 'P': 0}},
                2: {'K': {'B': 0, 'P': 0}, 
                    'Q': {'B': 0, 'P': 0},
                    'J': {'B': 0, 'P': 0}}}

    if player == 1:
        for i, card in enumerate(['K', 'Q', 'J']):
            strategy[1][card]['B'] = vector[1 + 4*i]
            strategy[1][card]['P'] = vector[2 + 4*i]
            if vector[2 + 4*i] != 0:
                strategy[2][card]['B'] = vector[3 + 4*i] / vector[2 + 4*i]
                strategy[2][card]['P'] = vector[4 + 4*i] / vector[2 + 4*i]

    if player == 2:
        # 1 is [Bet], 2 is [Check]
        for i, card in enumerate(['K', 'Q', 'J']):
            strategy[1][card]['B'] = vector[1 + 4*i]
            strategy[1][card]['P'] = vector[2 + 4*i]
            if vector[2 + 4*i] != 0:
                strategy[2][card]['B'] = vector[3 + 4*i] / vector[2 + 4*i]
                strategy[2][card]['P'] = vector[4 + 4*i] / vector[2 + 4*i]


    return strategy


x = np.array(
    [
        1,
        1,
        0,
        0,
        0,
        0,
        1,
        0.6667,
        0.3333,
        0.3333,
        0.6667,
        0,
        0.6667
    ]
)

y = np.array(
    [
        1,
        1,
        0,
        1,
        0,
        0.3333,
        0.6667,
        0,
        1,
        0,
        1,
        0.3333,
        0.6667
    ]
)




eq_strategy = {'B': {'K': {'B': 1, 'P': 0}, 
                        'Q': {'B': 1/3, 'P': 2/3},
                        'J': {'B': 0, 'P': 1}},

                               'P': {'K': {'B': 1, 'P': 0},
                                     'Q': {'B': 0, 'P': 1},
                                     'J': {'B': 1/3, 'P': 2/3}}}

# y = transform_strategy_to_vector(eq_strategy)

random_strategy = {'B': {'K': {'B': 0.5, 'P': 0.5}, 
                        'Q': {'B': 0.5, 'P': 0.5},
                        'J': {'B': 0.5, 'P': 0.5}},

                               'P': {'K': {'B': 0.5, 'P': 0.5},
                                     'Q': {'B': 0.5, 'P': 0.5},
                                     'J': {'B': 0.5, 'P': 0.5}}}





def get_player1_behav_equilibrium():
    # Max v = c[0], value of the game
    c = np.zeros((14,))
    c[0] = -1

    # Assert x is a valid strategy, add dummy column for v
    A_eq = g.get_infoset_strategies_matrix(1)
    A_eq = np.vstack((np.zeros(7,), A_eq.T)).T
    b_eq = np.zeros((7,))
    b_eq[0] = 1

    negative_column_constraints = (M2 @ g.get_infoset_strategies_matrix(2)) * -1
    A_ub = np.vstack((np.zeros(13,), negative_column_constraints.T)).T
    b_ub = np.zeros((13,))

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq)
    print(res)


# get_player1_behav_equilibrium()

def get_player1_best_response(strategy):
    y = transform_strategy_to_vector(strategy, player=2)
    
    # Minimize the negatives of payoff = Maximise payoff
    c = (M2 @ y) * -1
    
    # Assert sum of behavioural probabilities = 1
    A_eq = g.get_infoset_strategies_matrix(1)
    b_eq = np.zeros((7,))
    b_eq[0] = 1

    res = linprog(c, A_eq=A_eq, b_eq=b_eq)
   
    back_to_strategy = transform_vector_to_strategy(res.x, player=1)
    return back_to_strategy

def get_player1_exploitability(strategy):
    x = transform_strategy_to_vector(strategy, player=1)
    
    # Minimize the payoff for player 1
    c = (x @ M2)
    
    # Assert sum of behavioural probabilities = 1
    A_eq = g.get_infoset_strategies_matrix(2)
    b_eq = np.zeros((7,))
    b_eq[0] = 1

    res = linprog(c, A_eq=A_eq, b_eq=b_eq, method="revised simplex", options={"tol":0.1})
    return res.fun / 6

def get_player2_best_response(strategy):
    x = transform_strategy_to_vector(strategy, player=1)
    
    # Minimize the payoff for player 1
    c = (x @ M2)
    
    # Assert sum of behavioural probabilities = 1
    A_eq = g.get_infoset_strategies_matrix(2)
    b_eq = np.zeros((7,))
    b_eq[0] = 1

    res = linprog(c, A_eq=A_eq, b_eq=b_eq, method="revised simplex", options={"tol":0.1})
    back_to_strategy = transform_vector_to_strategy(res.x, player=2)
    return back_to_strategy

# [1,   a, 1-a, 1, 0,   0, 1, (a+1)/3, 1-(a+1)/3,   a/3, 1-a/3, 0, 1]



# print(transform_strategy_to_vector(p1_eq, player=1))