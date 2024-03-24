import argparse
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as pyplot


## Creating command line arguments pasrer,
#  defining required arguments and its parameters
#  and also providing help messages for each argument
#
#  Returns an argparse object with several attributes
#  containing user-provided data
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("ifile",
                        type=argparse.FileType('r'),
                        help='input file with measured data')
    parser.add_argument("distribution",
                        help='distribudion to use for calculations',
                        choices=['normal', 'Cauchy', 'uniform'])
    return parser.parse_args()

## Parsing and processing of command line arguments
args = parse_args()
distribution = args.distribution
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

## Calculating a number of equal intervals for histogram,
#  width of the interval and amount of measured values in each interval
bins = int(np.sqrt(len(sample)))
df = bins - 3
bin_width = (max(sample) - min(sample)) / bins
xh, yh, _ = pyplot.hist(sample, bins=bins, density=False, alpha=0.5)

## Calculating chi-square for the measured data
if distribution == 'Cauchy':
    loc, scale = stats.cauchy.fit(sample)
else:
    loc = np.mean(sample)
    scale = np.std(sample)
eps = [0] * bins
alpha = [0] * bins
P = [0] * bins
N = [0] * bins
x = [0] * bins
chi2_pr = 0

dist_dict = {
    'normal': stats.norm.pdf,
    'Cauchy': stats.cauchy.pdf
}

for i in range(bins):
    x[i] = yh[i] + bin_width / 2
    if distribution == 'uniform':
        N = [1 / (np.max(sample) - np.min(sample))] * bins
    else:
        N[i] = len(sample) * bin_width * dist_dict[distribution](x[i], loc, scale)
    chi2_pr = chi2_pr + ((N[i] - xh[i]) ** 2) / N[i]

## Printing the result
print("Practical chi-square value: ", chi2_pr)
