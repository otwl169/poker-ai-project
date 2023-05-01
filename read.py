### Read a results file and calculate statistics from trials
import os.path
from itertools import islice

class Read:
    def __init__(self, preliminary=False):
        self.RESULTS_DIR = "Results/"
        self.NUM_LINES = 20_000
        self.preliminary = preliminary

    def read_file(self, file):
        assert os.path.exists(file)

        with open(file, "r") as fh:
            print(file)
            lines = islice(fh, self.NUM_LINES)

            # Compute average
            total = 0.0
            for x in lines:
                total += float(x)
            
            print(total / self.NUM_LINES)
    
    def read_algorithm_data(self, algorithm):

        for opponent in ["random", "sophisticated", "dynamic", "equilibrium"]:
            if self.preliminary:
                self.NUM_LINES = 10_000
                file = "Preliminary Results/" + algorithm + "_" + opponent + "_" + f"{self.NUM_LINES//1000}k"     
            else:
                self.NUM_LINES = 20_000
                file = self.RESULTS_DIR + algorithm + "_" + opponent + "_" + f"{self.NUM_LINES//1000}k"
                
            self.read_file(file)


if __name__ == "__main__":
    Reader = Read(preliminary=False)
    Reader.NUM_LINES = 20_000
    # Reader.read_file("Preliminary Results/BEFFE_random_10k")
    # Reader.read_file("Preliminary Results/BEFFE_sophisticated_10k")
    # Reader.read_file("Preliminary Results/BEFFE_dynamic_10k")

    # Reader.read_file("Preliminary Results/MBEFFE_random_10k")
    # Reader.read_file("Preliminary Results/MBEFFE_sophisticated_10k")
    # Reader.read_file("Preliminary Results/MBEFFE_dynamic_10k")

    # Reader.read_file("Preliminary Results/BEFEWP_random_10k")
    # Reader.read_file("Preliminary Results/BEFEWP_sophisticated_10k")
    # Reader.read_file("Preliminary Results/BEFEWP_dynamic_10k")

    # Reader.read_file("Preliminary Results/MBEFEWP_random_10k")
    # Reader.read_file("Preliminary Results/MBEFEWP_sophisticated_10k")
    # Reader.read_file("Preliminary Results/MBEFEWP_dynamic_10k")



    # Reader.read_algorithm_data("BE")

    Reader.read_algorithm_data("BEFFE")

    Reader.read_algorithm_data("MBEFFE")

    # Reader.read_algorithm_data("BEFEWP")

    # Reader.read_algorithm_data("MBEFEWP")

    Reader.read_algorithm_data("PBR")
    