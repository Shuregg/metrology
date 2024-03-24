import argparse
import scipy.stats as stats


## Creating command line arguments pasrer,
#  defining required arguments and its parameters
#  and also providing help messages for each argument
#
#  Returns an argparse object with several attributes
#  containing user-provided data
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("bins",
                        help="a number of equal intervals in histogram")
    parser.add_argument("significance",
                        help="level of significance")
    return parser.parse_args()


## Parsing and processing of command line arguments
#  Arguments of the Student's t distribution inverse survival function:
#  df - degrees of freedom
#  q - significance level
args = parse_args()

try:
    df = int(args.bins)-2
except ValueError:
    print("Error: pass the first argument as an integer number")
    quit()
try:
    q = float(args.significance.replace(',', '.'))
except ValueError:
    print("Error: pass the second argument as a floating point value")
    quit()

## Printing the calculated result
print("Theoretical chi-square value: ", stats.t.isf(q=q/2, df=df))
