# (c) 2021 by William H. Grover  |  wgrover@engr.ucr.edu  |  groverlab.org

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('cairo')
from matplotlib.patches import Rectangle
from matplotlib.patches import ConnectionPatch

import numpy, scipy.stats, scipy.optimize
numpy.seterr(invalid='ignore')  # for suppressing log_10(0) warnings

plt.rcParams["font.family"] = "Helvetica"
# import matplotlib.font_manager as fm
# font = fm.FontProperties(family = 'Helvetica', fname = '/Library/Fonts/Helvetica.ttc')


f = plt.figure(figsize=(6,3), tight_layout=True)
ax1 = f.add_subplot(121)
ax2 = f.add_subplot(122)

def plot_it(prefix="", candycodes=[], color="", zorder=1):

    mean_max_shared_strings = []
    std_max_shared_strings = []
    max_max_shared_strings = []
    min_max_shared_strings = []
    mad_max_shared_strings = []
    iqr_max_shared_strings = []

    for c in candycodes:
        max_shared_strings = []
        print(prefix+str(c))
        f = open(prefix + str(c) + ".txt")
        for line in f:
            max_shared_strings.append(int(line[-2]))
        # print("  len = %i" % len(max_shared_strings))
        mean = numpy.mean(max_shared_strings)
        print("  mean = %f" % mean)
        std = numpy.std(max_shared_strings)
        # print("  std = %f" % std)
        max = numpy.max(max_shared_strings)
        # print("  max = %f" % max)
        min = numpy.min(max_shared_strings)
        # print("  min = %f" % min)
        mad = scipy.stats.median_abs_deviation(max_shared_strings)
        # print("  mad = %f" % mad)
        iqr = scipy.stats.iqr(max_shared_strings)
        # print("  iqr = %f" % iqr)
        mean_max_shared_strings.append(mean)
        std_max_shared_strings.append(std)
        max_max_shared_strings.append(max)
        min_max_shared_strings.append(min)
        mad_max_shared_strings.append(mad)
        iqr_max_shared_strings.append(iqr)

    candycodes = numpy.array(candycodes)
    mean_max_shared_strings = numpy.array(mean_max_shared_strings)
    std_max_shared_strings = numpy.array(std_max_shared_strings)
    max_max_shared_strings = numpy.array(max_max_shared_strings)
    min_max_shared_strings = numpy.array(min_max_shared_strings)
    mad_max_shared_strings = numpy.array(mad_max_shared_strings)
    iqr_max_shared_strings = numpy.array(iqr_max_shared_strings)

    # m, b = numpy.polyfit(numpy.log10(candycodes), mean_max_shared_strings, 1)
    # m, b = numpy.polyfit(numpy.log10(candycodes), mean_max_shared_strings,1)


    start = 1
    if "extra_colors/" in prefix:
        start = 2

    if len(candycodes[start:] > 1):
        def func(x, a, c):
            return a * numpy.log10(x) + c
        popt, pcov = scipy.optimize.curve_fit(func, candycodes[start:], mean_max_shared_strings[start:])
        print("%s:  y = %0.3f log_10(x) + %0.3f" % (prefix, popt[0], popt[1]))

        # trendlines
        ax1.plot(candycodes[start:], func(candycodes[start:], *popt), color=color,
                 linewidth=1)
        ax2.plot(numpy.append(candycodes[start:],1e20), func(numpy.append(candycodes[start:],1e20), *popt), color=color,
                 linewidth=1)

        # round markers
        ax1.plot(candycodes[start:], mean_max_shared_strings[start:], color=color, linestyle='None', marker="o",
                 markersize=5, zorder=zorder)
        ax2.plot(candycodes[start:], mean_max_shared_strings[start:], color=color, linestyle='None', marker="o",
                 markersize=3, zorder=zorder)

        # +/- 1 standard deviation error bars for the first plot:
        ax1.errorbar(candycodes[start:], mean_max_shared_strings[start:],
                     yerr=std_max_shared_strings[start:],
                     fmt="none", ecolor=color, capsize=3, linewidth=1, zorder=zorder)

        # +/- full range in 100 replicates
        # ax1.errorbar(candycodes[start:], mean_max_shared_strings[start:],
        #              yerr=(min_max_shared_strings[start:], max_max_shared_strings[start:]),
        #              fmt="none", ecolor=color, capsize=3)

    else:  # this is for the single plot:
        # Plot it on the first plot:
        ax1.plot(candycodes, mean_max_shared_strings, color=color, linestyle='None', marker="o", markersize=5, zorder=10)
        # but not the second plot:
        # ax2.plot(candycodes, mean_max_shared_strings, color=color, linestyle='None', marker="o", markersize=4)

        # +/- 1 standard deviation error bars:
        ax1.errorbar(candycodes, mean_max_shared_strings,
                     yerr=std_max_shared_strings,
                     fmt="none", ecolor=color, capsize=3, linewidth=1, zorder=zorder)

        # +/- full range in 100 replicates
        # ax1.errorbar(candycodes, mean_max_shared_strings,
        #              yerr=(min_max_shared_strings, max_max_shared_strings),
        #              fmt="none", ecolor=color, capsize=3)

    # full range error bars:
    # plt.errorbar(candycodes, mean_max_shared_strings,
    #              yerr=(mean_max_shared_strings - min_max_shared_strings,
    #                    max_max_shared_strings - mean_max_shared_strings),
    #              fmt="none", ecolor=style, capsize=3)


    # start = numpy.nonzero(numpy.rint(mean_max_shared_strings))[0][0] - 1

# y = 0 lines:
ax1.axhline(0, color='black', linewidth=0.5)
ax2.axhline(0, color='black', linewidth=0.5)

plot_it("biased_whites/", [1, 3, 10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000], "tab:red", zorder=4) # biased whites
plot_it("", [1, 3, 10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000], "tab:green", zorder=5)             # normal results
plot_it("extra_colors/", [1, 3, 10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000], "tab:blue", zorder=6)   # extra colors
plot_it("biased_whites/", [120], "k", zorder=10)    # 120 simulation

# ax1.plot(120, 2, "kx")    # 120 experimental results


###### MARKERS:

# The smallest number of matches from the six experimental match experiments was 21:
# ax2.plot([1, 1e10], [21, 21], "k-")
ax2.axhline(21, color='gray', linewidth=1, linestyle=(0, (1, 2)))
ax2.text(1, 17.4, "Smallest number of strings shared\nbetween two photos of the\nsame CandyCode", fontsize=7, multialignment="center", color="gray")

# # The largest number of matches from the six experimental match experiments was 32:
# ax2.plot([1, 1e10], [32, 32], "k-")

# # world population is 7.9 billion, 7.9x10^9
# # so for 1000 candycodes per person, need 7.9x10^15
# ax2.plot([7.95e12, 7.95e12], [0, 10], "k-")

# a random UUID has a 1% chance of collision after generating 3.26915E+17 codes:
# ax2.plot([3.26915E+17, 3.26915E+17], [0, 23], "k-")
ax2.axvline(3.26915E+17, color='gray', linewidth=1, linestyle=(0, (1, 2)))
ax2.text(2.0e12, 2.0, "1% chance\nof collision\nin v4 UUIDs", fontsize=7, rotation=0, color="gray", multialignment="right")
# dashed version:  linestyle=(0, (4, 4)))

# a random UUID uses 122 random bits, 2^122 = 5.3x10^36
# ax2.plot([5.3e36, 5.3e36], [0, 23], "k-")

# annotation of 120 simulation:L
ax1.annotate("Simulation of\n120 CandyCode\ntest library",
                  xy=(120, 2.8), xycoords='data',
                  xytext=(15, 5), textcoords='data',
                  size=7, va="center", ha="center",
                #   bbox=dict(boxstyle="round", fc="w", linewidth=0.5),
                  arrowprops=dict(arrowstyle="->",
                                  connectionstyle="arc3,rad=-0.3",
                                  fc="w"),
                  )



ax1.set_xscale('log')
ax1.set_xlim(1.5, 2e5)
ax1.set_ylim(-0.5,6.5)
ax1.set_xticks([10, 100, 1000, 10000, 100000])
# ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax1.set_xlabel(" . ", color="white")
ax1.set_ylabel("Largest number of strings shared\nbetween any two different CandyCodes")

ax2.set_xscale('log')
ax2.set_xlabel(" . ", color="white")
ax2.set_xticks([1, 1e5, 1e10, 1e15, 1e20])
ax2.set_xlim((0.1, 1e21)) 
# ax2.set_ylim((-1,25))

# plt.xlim((1, 1e50))
# plt.ylim((0, 40))

# callout rectangle in second plot:
ax2.plot((1,3e5,3e5,1,1), (-0.5,-0.5,6.5,6.5,-0.5), "k-", linewidth=0.5)

con = ConnectionPatch(
    xyA=(1,-0.5), coordsA=ax2.transData,
    xyB=(2e5,-0.5), coordsB=ax1.transData,
    linewidth=0.5)
f.add_artist(con)

con = ConnectionPatch(
    xyA=(1,6.5), coordsA=ax2.transData,
    xyB=(2e5, 6.5), coordsB=ax1.transData,
    linewidth=0.5)
f.add_artist(con)

ax1.text(1.5e2, 3.3, "8 nonpareil colors, 5x whites", fontsize=8, rotation=39, color="tab:red", fontweight="bold")
ax1.text(2.0e3, 2.1, "8 nonpareil colors", fontsize=8, rotation=28, color="tab:green", fontweight="bold")
ax1.text(1.3e3, 0.6, "15 nonpareil colors", fontsize=8, rotation=22, color="tab:blue", fontweight="bold")

ax2.text(7.0e5, 7.9, "8 nonpareil colors, 5x whites", fontsize=8, rotation=44.5, color="tab:red", fontweight="bold")
ax2.text(1.0e6, 5.9, "8 nonpareil colors", fontsize=8, rotation=37, color="tab:green", fontweight="bold")
ax2.text(1.0e6, 3.8, "15 nonpareil colors", fontsize=8, rotation=28, color="tab:blue", fontweight="bold")

ax1.text(2, 5.94, "A", fontsize=12, fontweight="bold")
ax2.text(0.3, 22.8, "B", fontsize=12, fontweight="bold")

# Shared x-axis:
f.text(0.53,0.06, "Total number of CandyCodes in library (logarithmic scale)", ha="center")

plt.savefig("sim_plot.pdf")



