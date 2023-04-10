# Plan going forwards (week 7- end of week 8)

1) Create LPs for gift strategy and full exploitation
2) Implement DBBR modelling, and allow for a model to be exploited using LPs

3) Read and implement MIVAT algorithm for 3 card Kuhn poker
4) Combine gift strategy value and mivat estimator -> use value expected from MIVAT instead of / in conjuction with gift value

HOPEFUL:

5) Implement 6 card or such Kuhn poker
6) Implement some version of CFR to compute equilibria for both players
7) Implement DBBR algorithm for 6 card poker
8) Combine DBBR with MIVAT trained for 6 card Kuhn poker in a similar manner to safe opponent exploitation
9) Look at how linus deals with computing gifts in his version of safe exploitation and perhaps implement something similar

EVALUATION:

Evaluate how MIVAT performs on 3-card kuhn poker. 
    Does it give an accurate estimator? 
    How does its use improve or change safe exploitation?

Evaluate how MIVAT performs on 6-card kuhn poker
    Does it give an accurate estimator?
    How does its use improve or change safe exploitation?

PRESENTATION:

1) Cover topics such as CFR, card and action abstrations, informations sets all briefly.
   Also cover monte carlo estimation, all necessary information for MIVAT
2) Introduce the idea of safe exploitation and explain the difficulty
3) Introduce 3-card kuhn poker, a simple game
4) Show how safe opponent exploitation performs in 3-card domain
5) Show how also using MIVAT performs in 3-card domain
6) Introduce 6-card kuhn poker, show how CFR is needed as it is difficult to compute Nash equilibria -> explain reasoning behind
choosing it (making problem harder only increases time needed to make deductions about algorithm performance)
7) Introduce the idea of opponent modelling
8) Brief overview of DBBR
9) Overview of limitations of safe exploitation paper when it comes to larger games
10) Show how MIVAT exploitation performs in 6-card domain

## Algorithm

Implement Extensive form RWYWE, BEFEWP, BEFFE.

Modified RWYWE, BEFEWP, BEFFE:

For X = 100, 500, 1000, 5000, 10000

    Update rule for gift strategy value uses expected value of nemesis until exploitative has played against opponent for X iterations.
    From then on uses the value of MIVAT estimator.

