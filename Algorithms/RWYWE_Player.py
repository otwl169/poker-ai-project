from Kuhn import Kuhn, Card, Action
from Modelling.DBBR import DBBR_Model
import random


class RWYWE_Player:
    # Note that only played from Player 1's perspective

    def __init__(self):
        # Value of the game to player i
        self.v = -1/18

        # Total accumulated gift strategy value
        self.k = 0

        # Opponent model M
        self.M = Model()
    
    def play(self, history: list(Action)):
        pi_t = 