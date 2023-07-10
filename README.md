# Poker AI Project

Implementation of Poker AI techniques for CS310 Project.

## Kuhn Poker

Code for Kuhn poker implementation is included in Kuhn.py

## Player types

RandomPlayer: Chooses a random legal move at each information set

OptimalPlayer: Plays a Nash equilibrium strategy parameterised on alpha

SophisticatedPlayer: Plays with probabilities within 0.2 of a Nash equilibrium strategy at each information set

DynamicPlayer: Plays a uniform random strategy for first 100 rounds then swaps to an interval best response to your strategy for the rest of the game. Unrealistically strong as is given your exact strategy at each interval.

## Opponent Models

Results use model which is given the player's card at end of each round.

Also coded is the DBBR (Deviation Based Best Response) algorithm which is given no private information and uses intuition that a player plays their public history with private information sorted according to the probability of the action being taken with each private information within an equilibrium strategy.

## LinearProgram

Uses convex optimization library CVXPY to find exact best responses and best equilibrium responses to strategies.