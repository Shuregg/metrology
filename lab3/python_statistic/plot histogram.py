import numpy as np
import argparse
import matplotlib.pyplot as pyplot
import matplotlib.mlab as mlab
import scipy.stats as stats


## Creating command line arguments pasrer,
#  defining required arguments and its parameters
#  and also providing help messages for each argument
#
#  Returns an argparse object with several attributes
#  containing user-provided data
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("ifile",
                        help='input file with measured data',
                        type=argparse.FileType('r'))
    parser.add_argument("distribution",
                        help='name of the distribution to plot',
                        choices=['normal', 'Cauchy', 'uniform'])
    return parser.parse_args()


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


## Plot probability density function of normal distribution
#  using measured data parameters:
#  mu -- mean value of measured data,
#  sigma -- standart deviation of measured data
#  Arguments:
#      sample -- an array measured data
#  Return array-like object of function values the same size as x
def normal(sample):
    x = np.linspace(np.min(sample)-1, np.max(sample)+1, len(sample)*20)
    mu = np.mean(sample)
    sigma = np.std(sample)
    y_norm = stats.norm.pdf(x, mu, sigma)
    return x, y_norm


## Plot probability density function of Cauchy's distribution
#  using measured data parameters:
#  mu -- mean value of measured data,
#  sigma -- standart deviation of measured data
#  Arguments:
#      sample -- an array measured data
#  Return array-like object of function values the same size as x
def Cauchy(sample):
    df = 1
    x = np.linspace(np.min(sample)-1, np.max(sample)+1, len(sample)*20)
    tmp, loc, scale = stats.t.fit(sample, df)
    y_st = stats.t.pdf(x, df, loc=loc, scale=scale*0.95)
    return x, y_st


## Plot probability density function of uniform distribution using
#  measured data parameters:
#  mu -- mean value of measured data,
#  sigma -- standart deviation of measured data
#  Arguments:
#      sample -- an array measured data
#  Return array-like object of function values the same size as x
def uniform(sample):
    x = np.linspace(np.min(sample)-1, np.max(sample)+1, len(sample)*2)
    diff = np.max(sample) - np.min(sample)
    y_ln = np.linspace(1/diff, 1/diff, len(sample)*2)
    return x, y_ln


dist_dict = {
    'normal': normal,
    'Cauchy': Cauchy,
    'uniform': uniform
}

## Calculating histogram values of the measured data
bins = int(np.sqrt(len(sample)))
bin_width = (max(sample)-min(sample))/bins
xn, yn, _ = pyplot.hist(sample, bins=bins, density=True, alpha=0)
xh, yh, _ = pyplot.hist(sample, bins=bins, density=False,  alpha=0.7,
                        color='green', label='measured data')

# Create a range for calculating distribution
x, y = dist_dict[args.distribution](sample)
scale = xh[0]/xn[0]

pyplot.plot(x, y*scale, 'b--', label=args.distribution + ' distribution')
pyplot.xlabel('Bins')
pyplot.ylabel('Number of values within the range of bin')
pyplot.xlim(min(sample), max(sample))
pyplot.ylim(0, max(xh)*1.05)
pyplot.grid(True)
pyplot.legend(loc='upper right')

pyplot.show()
