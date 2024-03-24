import scipy as sp
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt

def print_stats(sample):
    print("Mean", mean(sample))
    print("Minimum value", min(sample))
    print("Maximum value", max(sample))
    print("Deviation", sigma(sample))
    print("Number of elements", len(sample))
    print("Median", sorted(sample)[len(sample) // 2])
    print("Variance", sigma(sample) ** 2)
    print("Kurtosis", sp.stats.kurtosis(sample))
    print("Skew", sp.stats.skew(np.array(sample)))

def mean(selection_):
    return 1 / len(selection_) * sum(selection_)

def sigma(selection_):
    sum = 0
    m = mean(selection_)
    for X in selection_:
        sum += (X - m) ** 2
    return (1 / (len(selection_) - 1) * sum) ** (1 / 2)

def sample_handler(filename):
    filename_plus_format = filename+'.txt'
    miss = True
    file = open(filename_plus_format, "r")
    sample_raw = []
    sample_mod = sample_raw
    summ = 0
    # init sample list from file
    for x in file:
        sample_raw.append(float(x))
    mean_raw = mean(sample_raw)
    deviation_raw = sigma(sample_raw)
    mean_mod = mean_raw
    deviation_mod = deviation_raw
    print(f'\nRaw {filename} stats:')
    print_stats(sample_raw)

    while miss:
        miss = False
        for x in sample_mod:
            if abs(float(x) - mean_mod) >= 3 * deviation_mod:
                miss = True
                sample_mod.remove(x)
                print(x)
                break

        mean_mod = mean(sample_mod)
        deviation_mod = sigma(sample_mod)
    print(f'\nSample without misses (saved to {filename}_no_misses.txt)')
    print_stats(sample_mod)
    # Write modified sample to file
    with open(f'{filename}_no_misses.txt', "w") as file:
        for  line in sample_mod:
            file.write(str(line) + '\n')
    return sample_mod

# ==========================================================================
def normal(sample):
    x = np.linspace(np.min(sample)-1, np.max(sample)+1, len(sample)*20)
    mu = np.mean(sample)
    sigma = np.std(sample)

    y_norm = sp.stats.norm.pdf(x, mu, sigma)
    return x, y_norm

def Cauchy(sample):
    df = 1
    x = np.linspace(np.min(sample)-1, np.max(sample)+1, len(sample)*20)
    tmp, loc, scale = sp.t.fit(sample, df)
    y_st = sp.t.pdf(x, df, loc=loc, scale=scale*0.95)
    return x, y_st

def uniform(sample):
    x = np.linspace(np.min(sample)-1, np.max(sample)+1, len(sample)*2)
    diff = np.max(sample) - np.min(sample)
    y_ln = np.linspace(1/diff, 1/diff, len(sample)*2)
    return x, y_ln

def plot_sample_dist(sample, distribution_type='normal', sample_name='Sample', nrows_=1, ncols_=1):
    # plt.figure(figsize=(6, 6))
    # for i in range (nrows_ * ncols_):
    #     plt.subplot(nrows_, ncols_, i)

    ## Calculating histogram values of the measured data
    bins = int(np.sqrt(len(sample)))
    bin_width = (max(sample)-min(sample))/bins
    xn, yn, _ = plt.hist(sample, bins=bins, density=True, alpha=0)
    xh, yh, _ = plt.hist(sample, bins=bins, density=False,  alpha=0.7,
                            color='green', label='measured data')
    # Create a range for calculating distribution
    match distribution_type:
        case "normal":
            x, y = normal(sample)
        case "Cauchy":
            x, y = Cauchy(sample)
        case "cauchy":
            x, y = Cauchy(sample)
        case "uniform":
            x, y = uniform(sample)
    
    # fig = plt.figure(figsize=(6, 6))
    # fig, axes = plt.subplots(nrows=nrows_, ncols=ncols_, figsize=(6, 6))
    scale = xh[0]/xn[0]
    plt.plot(x, y*scale, 'b--', label=f'{distribution_type} distribution')
    plt.title(f'{sample_name}')
    plt.xlabel('Bins')
    plt.ylabel('Number of values within the range of bin')
    plt.xlim(min(sample), max(sample))
    plt.ylim(0, max(xh)*1.05)
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.show()
# ===============================================================================
# @                                MAIN CODE                                    @
# ===============================================================================
    
file_names = ['sample_1_1', 'sample_1_2', 'sample_3', 'sample_kz']
samples = []
for i in range (len(file_names)):
    samples.append(sample_handler(file_names[i]))

for i in range (len(samples)):
    plot_sample_dist(samples[i], "normal", file_names[i], i, 1)
