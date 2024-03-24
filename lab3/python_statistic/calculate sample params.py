import argparse
import numpy as np
import pandas
from collections import OrderedDict
import scipy.stats as st

## Creating command line arguments pasrer,
#  defining required arguments and its parameters
#  and also providing help messages for each argument
#
#  Returns an argparse object with several attributes
#  containing user-provided data
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("ifile", type=argparse.FileType('r'),
                        help='input file with measured data')
    return parser.parse_args()


## Basic calculations of measured data parameters.
class ParamCalc:

    ## The constructor
    #
    #  Arguments:
    #      sample -- an array measured data
    def __init__(self, sample):
        self.sample = sample

    ## Returns the mean value of measured data sample
    #  Return type: numpy.float64
    def mean(self):
        return np.mean(self.sample)

    ## Returns the standart deviation of measured data sample
    #  Return type: numpy.float64
    def std(self):
        return np.std(self.sample)

    ## Returns the standart deviation of the mean for measured data sample
    #  Return type: numpy.float64
    def std_of_mean(self):
        return self.std() / np.sqrt(self.count())

    ## Returns the minimum value of measured data sample
    #  Return type: float
    def min(self):
        return min(self.sample)

    ## Returns the maximum value of measured data sample
    #  Return type: float
    def max(self):
        return max(self.sample)

    ## Returns the number of elements for measured data sample
    #  Return type: int
    def count(self):
        return len(self.sample)

    ## Returns the median of measured data sample
    #  Return type: numpy.float64
    def median(self):
        return np.median(self.sample)

    ## Returns the variance of measured data sample
    #  Return type: numpy.float64
    def var(self):
        return np.var(self.sample)

    def skew(self):
        return st.skew(self.sample)

    def kurtosis(self):
        return st.kurtosis(self.sample)


## Parsing and processing of command line arguments
args = parse_args()
sample = args.ifile.readlines()
if len(sample) is not 0:
    for i in range(len(sample)):
        try:
            sample[i] = float(sample[i].replace(',', '.'))
        except ValueError:
            print("Error: input file must contain floating point numbers only")
            quit()
else:
    print("Error: provided an empty input file")
    quit()

pc = ParamCalc(sample)

sdict = OrderedDict()
sdict['Mean'] = pc.mean()
sdict['Minimum value'] = pc.min()
sdict['Maximum value'] = pc.max()
sdict['Standard deviation'] = pc.std()
sdict['Number of elements'] = pc.count()
sdict['Median'] = pc.median()
sdict['Standard deviation of the mean'] = pc.std_of_mean()
sdict['Variance'] = pc.var()
sdict["Skew"] = pc.skew()
sdict["Kurtosis"] = pc.kurtosis()

print("Parameters of the given sample:",
      pandas.DataFrame({'': list(sdict.values())}, sdict.keys()))
