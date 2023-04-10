# Mivat paper

## Goal

 - Evaluate an agents performance
 - Traditionally Monte Carlo estimation is used, with independent trials and average of its performance as an estimate
 - Paper suggests a technique which not only uses the utility of each trial, but the complete history of interaction
 - This technique should reduce the variance of the estimator, provided a good value function is used
 - Shown to achieve dramatic variance reduction in evaluating play for two-player Limit Texah Hold'em

## Approach

 - Machine learning to find a value function
 - Define an optimization to minimize estimators variance on a set of training data
 - Agent evaluation attempts to find the estimated utility of a player given a strategy profile. This is useful in the case where you cannot enumerate all the terminal histories to calculate this value directly

 ## Monte Carlo Estimation

  - Simply an average of the utility from T trials
  - Variance is simply the variance of utility from a strategy profile
  - In poker, the stdev of a players outcome is around $6 and a typical 
  desired precision is around $0.05
  - To achieve this desired precision, more than 50,000 trials would have to be observed -> impractical for any human opponents

## Improvements to Monte Carlo Estimation

 - Find a better estimate of per-trial utility. Identify a real-valued function on terminal histories for which the expected value of this function is equal to the expected utility. 
 - This is an unbiased estimator of utility.
 - If this estimator has a lower variance than the utility, it can be used instead to give a better estimator

## Advantage-sum estimators

 - Given some real-valued function on histories Vj:
    - Define a real-valued function on terminal histories:
    - Svj, skill is the sum of the values of terminal histories - sum of values of preceding history where the action isnt from chance
    - Lvj, the opposite
    - Pvj, Vj(empty set)
    - The advantage sum estimator is now Svj + Pvj
    - Utility is equal to Svj + Lvj + Pvj
    - If the expected value of the luck constraint is 0, then we have defined an unbiased estimator (zero-luck constraint)

## MIVAT approach

 - Learn a good value function from past interactions between players
 - Define an optimization for finding the ideal value function
 - Map histories to a vector of d features
 - Vj(history) = map(history -> d-dimensional feature vector) * d-dimensional theta
 
## Setup

 - Define a function to map histories to a vector of d features:
    - In Kuhn poker, we have 1: Card strength. 2: Pot equity. 3: Pot value
 - Train on a series of examples:
    - Calculate At for each example. Store payout at each example
    - Directly solve for theta j using matrices of these samples
    - Use theta j in estimator


## Results

Money AVG and STdev:
100,000 trials. 1.2695913673304495 Stdev. 0.05248 Mean +- 0.00787

2D_eq_eq
Stdev Money: 1.2695913673304495, Stdev Est: 0.9113651705351027

6D_eq_eq
Stdev Money: 1.270025924774766, Stdev Est: 0.8891157615754116

6D_eq_eq CI:
Sample 50:  95% Confidence Interval: ± 0.246
Sample 100: 95% Confidence Interval: ± 0.174
Sample 500: 95% Confidence Interval: ± 0.0779
Sample 1000: 95% Confidence Interval: ± 0.0551
Sample 5000: 95% Confidence Interval: ± 0.0246
Sample 10000: 95% Confidence Interval: ± 0.0174
Sample 100000: 95% Confidence Interval: ± 0.00551

