### Read a results file and calculate statistics from trials
import os.path
from itertools import islice


RESULTS_FILE = "Results/BEFFE_sophisticated_10k"
NUM_LINES = 10_000

assert os.path.exists(RESULTS_FILE)

with open(RESULTS_FILE, "r") as fh:
    lines = islice(fh, NUM_LINES)

    # Compute average
    total = 0.0
    for x in lines:
        total += float(x)
    
    print(total / NUM_LINES)

