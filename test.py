from Kuhn import *

# Import algorithms
from Algorithms.BEFFE import BEFFE_Player
from Algorithms.MBEFFE import MBEFFE_Player

from Algorithms.BEFEWP import BEFEWP_Player
from Algorithms.MBEFEWP import MBEFEWP_Player

from Algorithms.Best_Equilibrium import BE_player
from Algorithms.Pure_Best_Response import BR_Player

# Import opponent classes
from Opponents.OptimalPlayer import OptimalPlayer
from Opponents.RandomPlayer import RandomPlayer
from Opponents.SophisticatedPlayer import SophisticatedPlayer
from Opponents.DynamicPlayer import DynamicPlayer

# Import OS to check if file exists
import os.path
import time

import pickle

from MIVAT.MIVAT import MIVAT

class Test:
    def __init__(self, preliminary = False):
        
        self.RESULTS_FILE = "Results/BEFFE_dynamic_20k"
        self.number_of_tests = 20_000
        self.number_of_hands = 1000
        self.preliminary = preliminary

        if preliminary:
            self.number_of_tests = 10_000

        # Load pretrained MIVAT weights
        with open("MIVAT/6D_eq_eq_mivat_theta", "rb") as f:
            theta = pickle.load(f)

        
        self.estimator = MIVAT(theta)

    def get_game(self, algorithm, opponent):
        # Determine algorithm to test and opponents, and return game with those players
        if algorithm == "BEFFE":
            p1 = BEFFE_Player(self.number_of_hands)
        elif algorithm == "MBEFFE":
            p1 = MBEFFE_Player(self.number_of_hands, self.estimator)
        elif algorithm == "BEFEWP":
            p1 = BEFEWP_Player(self.number_of_hands)
        elif algorithm == "MBEFEWP":
            p1 = MBEFEWP_Player(self.number_of_hands, self.estimator)
        elif algorithm == "BE":
            p1 = BE_player()
        elif algorithm == "PBR":
            p1 = BR_Player()
        else:
            print("Algorithm must be one of five types")
            exit(1)
        
        dynamic = False
        if opponent == "random":
            p2 = RandomPlayer()
        elif opponent == "sophisticated":
            p2 = SophisticatedPlayer()
        elif opponent == "dynamic":
            p2 = DynamicPlayer()
            dynamic = True
        elif opponent == "equilibrium":
            p2 = OptimalPlayer()
        else:
            print("Opponent must be one of four types")
            exit(1)

        return Kuhn(p1, p2, dynamic)

    def set_results_file(self, algorithm, opponent):
        assert algorithm in ["BEFFE", "MBEFFE", "BE", "BEFEWP", "MBEFEWP", "PBR"]
        assert opponent in ["random", "sophisticated", "dynamic", "equilibrium"]

        if not self.preliminary:
            self.RESULTS_FILE = "Results/" + algorithm + "_" + opponent + "_" + f"{self.number_of_tests//1000}k"
        else:
            self.RESULTS_FILE = "Preliminary Results/" + algorithm + "_" + opponent + "_" + f"{self.number_of_tests//1000}k"

    def run_test(self, algorithm, opponent):
        # Open text file to write results to
        self.set_results_file(algorithm, opponent)
        assert not os.path.exists(self.RESULTS_FILE)

        t1 = time.time()
        print(f"Testing {self.RESULTS_FILE}")
        with open(self.RESULTS_FILE, "a") as fh:
            buffer = []
            for i in range(self.number_of_tests):
                # Set the random seed to ensure same opponent strategies and card deals
                random.seed(i)

                # Play 1000 hands against opponent
                g = self.get_game(algorithm, opponent)
                for _ in range(self.number_of_hands):
                    (payoff, terminal_history) = g.play_round()
                
                buffer.append(g.player1_value / 1000)
                if len(buffer) >= 1000:
                    # Write to file
                    fh.write('\n'.join(map(str, buffer)) + '\n')
                    tn = time.time()
                    print(f"Test {i+1} completed in {tn-t1} time")
                    buffer = []
            
            fh.write('\n'.join(map(str, buffer)) + '\n')

        t2 = time.time()
        print(f"Finished testing {self.RESULTS_FILE} in {t2 - t1} time")


if __name__ == "__main__":
    Tester = Test(preliminary=False)

    # Tester.run_test("BEFFE", "random")
    # Tester.run_test("BEFFE", "sophisticated")
    # Tester.run_test("BEFFE", "dynamic")
    # Tester.run_test("BEFFE", "equilibrium")

    # Tester.run_test("MBEFFE", "random")
    # Tester.run_test("MBEFFE", "sophisticated")
    # Tester.run_test("MBEFFE", "dynamic")
    # Tester.run_test("MBEFFE", "equilibrium")

    # Tester.run_test("BE", "random")
    # Tester.run_test("BE", "sophisticated")
    # Tester.run_test("BE", "dynamic")
    # Tester.run_test("BE", "equilibrium")

    # Tester.run_test("PBR", "random")
    # Tester.run_test("PBR", "sophisticated")
    Tester.run_test("PBR", "dynamic")
    # Tester.run_test("PBR", "equilibrium")

    # Tester.run_test("BEFEWP", "random")
    # Tester.run_test("BEFEWP", "sophisticated")
    # Tester.run_test("BEFEWP", "dynamic")
    # Tester.run_test("BEFEWP", "equilibrium")

    Tester.run_test("MBEFEWP", "random")
    Tester.run_test("MBEFEWP", "sophisticated")
    Tester.run_test("MBEFEWP", "dynamic")
    # Tester.run_test("MBEFEWP", "equilibrium")