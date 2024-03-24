import argparse
import scipy.stats as stats
import numpy as np


## Creating command line arguments pasrer,
#  defining required arguments and its parameters
#  and also providing help messages for each argument
#
#  Returns an argparse object with several attributes
#  containing user-provided data
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("significance",
                        help="level of significance")
    return parser.parse_args()


## Parsing and processing of command line arguments
args = parse_args()
try:
    significance = float(args.significance.replace(',', '.'))
except ValueError:
    print("Error: pass the argument as an floating point value")
    quit()

## Printing a result to command line
print("Quantile of the Kolmogorov's distribution : ",
      stats.kstwobign.ppf(1 - significance))
