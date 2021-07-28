import matplotlib.pyplot as plt
import numpy
import random, math
import scipy.spatial
import sys

make_plots = False
verbose = False

remove_edges = True        # False -> True definitely better
min_colors = 4              # 3 -> 4 seems better.  fails at 5.
remove_duplicates = False    # True -> Doesn't matter if min_colors = 4

total_good_codes = 0
total_discards_too_few_colors = 0
total_discards_on_edge = 0

name = {"R":"red",
        "P":"pink",
        "O":"orange",
        "Y":"yellow",
        "G":"lightgreen",
        "L":"lightblue",
        "D":"dodgerblue",
        "W":"white" }

textcolor = {"R":"black",
             "P":"black",
             "O":"black",
             "Y":"black",
             "G":"black",
             "L":"black",
             "D":"black",
             "W":"black"}

if make_plots:
    fig, ax = plt.subplots(figsize=(4, 4)) 

# for x, y in numpy.random.random_sample((10, 2))-0.5:
#     print(x, y)
#     circle = plt.Circle((x, y), 0.1, fill=False)
#     ax.add_patch(circle)

# plt.xlim([-0.5, 0.5])
# plt.ylim([-0.5, 0.5])
# plt.show()

class candy():
    """The candy object represents a single nonpareil and its color/location/etc.
    A single candycode consists of several candy objects.
    """
    def __init__(self, id, color, x, y):
        self.id = id
        self.color = color
        self.x = x
        self.y = y
        self.neighbors = []
        self.discarded_because_on_edge = False
        self.discarded_because_too_few_colors = False
        self.string = ""  # a place to store this candy's successful string

class candycode:
    """The candycode object represents a single candycode.
    It contains several individual candy objects.
    """

    def __init__(self, id, colors, xs, ys):
        self.id = id
        candy_id = 0
        self.number_of_candies = 0
        self.candies = []
        self.strings = []
        for color, x, y in zip(colors, xs, ys):
            self.candies.append(candy(candy_id, color, float(x), -float(y)))
            candy_id += 1
            self.number_of_candies += 1
            
    def triangulate(self):
        """Method for converting the candycode to its string representation."""
        global total_good_codes, total_discards_on_edge, total_discards_too_few_colors
        # print("\u001b[33m%s:\u001b[0m\n" % self.filename)
        good_codes = 0
        discards_too_few_colors = 0
        discards_on_edge = 0
        self.tri = scipy.spatial.Delaunay([[c.x, c.y] for c in self.candies])
        for center in self.candies:
            on_edge = False
            too_few_colors = False
            if verbose:
                print("   %i: %s (%0.1f %0.1f)" % (center.id, center.color, center.x, center.y))
            if center.id in self.tri.convex_hull:
                on_edge = True
            indptr, indices = self.tri.vertex_neighbor_vertices
            for n in indices[indptr[center.id]:indptr[center.id+1]]:
                neighbor = self.candies[n]
                neighbor.theta = math.atan2(neighbor.y-center.y, neighbor.x-center.x)
                center.neighbors.append(neighbor)
            center.neighbors.sort(key=lambda x: x.theta, reverse=True)  # reverse = clockwise
            # order = {"R":0, "P":1, "O":2, "Y":3, "G":4, "L":5, "D":6, "W":7}  # rainbow
            order = {"R":5, "P":4, "O":3, "Y":7, "G":1, "L":2, "D":0, "W":6}  # alpha
            colorsort = sorted(center.neighbors, key=lambda x: order[x.color])
            top_neighbor_id = colorsort[0].id
            while center.neighbors[0].id != top_neighbor_id:
                center.neighbors = center.neighbors[1:] + center.neighbors[:1]  # rotate by 1
            if verbose:
                for n in center.neighbors:
                    print("      %i: %s (%0.1f %0.1f) %0.1f" % (n.id, n.color, n.x, n.y, n.theta))
            code_string = center.color + ''.join([n.color for n in center.neighbors])
            if len(set(code_string)) < min_colors:
                too_few_colors = True
            if on_edge and remove_edges:
                if verbose:
                    print("\u001b[31m      Discarded because on edge\033[0m\n")
                discards_on_edge += 1
                total_discards_on_edge += 1
                center.discarded_because_on_edge = True
            elif too_few_colors:
                if verbose:
                    print("\u001b[31m      Discarded because too few colors\033[0m\n")
                discards_too_few_colors += 1
                total_discards_too_few_colors += 1
                center.discarded_because_too_few_colors = True
            else:
                self.strings.append(code_string)
                center.string = code_string  # save the string with the candy too
                if verbose:
                    print("\u001b[32m      Good code\033[0m\n")
                good_codes += 1
                total_good_codes += 1
        if remove_duplicates:
            self.strings = list(set(self.strings))  # remove duplicates
        self.strings.sort()
        if verbose:
            print("   Good codes:", end="")
            for s in self.strings:
                print(" %s" % s, end="")
            print()
            print("      %i good codes\n" % good_codes +
                   "      %i discards because on edge\n" % discards_on_edge +
                   "      %i discards because too few colors\n" % discards_too_few_colors)
        
        # Individual candy plots:
        if make_plots:
            plt.axis("off") 
            plt.tight_layout()
        
            # Plot the triangular mesh:
            plt.triplot([c.x for c in self.candies], [c.y for c in self.candies],
                    self.tri.simplices, color="0.75")
        
            for c in self.candies:
                
                # Plot the candy vertices:
                plt.plot(c.x, c.y, "o", markersize=10, markeredgewidth=0.5,
                         color=name[c.color], markeredgecolor="k")

                # # Plot the candy ID:
                # plt.text(c.x, c.y, c.id, color=textcolor[c.color],
                #          horizontalalignment='center', verticalalignment='center',
                #          fontsize=11)

                # Plot the color letter:
                span = (plt.ylim()[1] - plt.ylim()[0]) # corrects misalignment
                plt.text(c.x, c.y-0.003*span, c.color, color=textcolor[c.color],
                         horizontalalignment='center', verticalalignment='center',
                         fontsize=7)
                
                # Mark the discards:
                if c.discarded_because_on_edge:
                    plt.plot(c.x, c.y, "_", markersize=10, color="k",
                             markeredgewidth=0.5)
                if c.discarded_because_too_few_colors:
                    plt.plot(c.x, c.y, "_", markersize=10, color="k",
                             markeredgewidth=0.5)
                
                # Plot the strings for the candies that have them:
                if not c.discarded_because_too_few_colors and not c.discarded_because_too_few_colors:
                    plt.text(c.x, c.y-0.03*span, c.string, color="k",
                             horizontalalignment='center', verticalalignment='center',
                             fontsize=5)

            # add candy ID to lower-right corner:
            plt.text(0.9, 0.1, self.id, horizontalalignment="center", verticalalignment="center",
                     transform = ax.transAxes)
            
            plt.savefig("" + str(self.id) + ".PDF")
            plt.clf()

candycodes = []

runs = 10
if len(sys.argv) > 1:
    runs = int(sys.argv[1])
    repeat_id = int(sys.argv[2])

print("Generating candycodes...")
for i in range(runs):
    # print("Generating candycode %i / %i" % (i, runs))
    xs = []
    ys = []
    colors = []
    while len(xs) < 94:   # This is the target number of candies per candycode; was 80
        x = 1
        y = 1
        while math.sqrt( (x-0.5)**2 + (y-0.5)**2) > 0.5:  # place candies in a circle
            x = random.random()
            y = random.random()
        keep = True
        for kx, ky in zip(xs, ys):
            if math.sqrt( (kx-x)**2 + (ky-y)**2 ) < 0.075:  # maximum spacing; was 0.080
                keep = False
                break
        if keep:
            xs.append(x)
            ys.append(y)
            colors.append(random.choice("RPOYGLDW"))   # unbiased color selection
            # colors.append(random.choice("RPOYGLDWWWWW"))   # 5x whites to match 120 experiment

    c = candycode(i, colors, xs, ys)
    c.triangulate()
    candycodes.append(c.strings)   # not full candycode objects







# # basic candycode statistics
# numbers_of_candies = []
# for c in candycodes:
#     print("%s: %i" % (c.id, c.number_of_candies))
#     numbers_of_candies.append(c.number_of_candies)

# numbers_of_candies = numpy.array(numbers_of_candies)
# print("Number of candycodes:", len(numbers_of_candies))
# print("Mean number of candies per candycode:", numpy.mean(numbers_of_candies))
# print("Median number of candies per candycode:", numpy.median(numbers_of_candies))
# print("Max number of candies per candycode:", numpy.max(numbers_of_candies))
# print("Min number of candies per candycode:", numpy.min(numbers_of_candies))





print("Comparing candycodes...")
largest_shared_strings = 0
for i1, s1 in enumerate(candycodes):
    for i2, s2 in enumerate(candycodes):
        if i2 > i1:   # just do a diagonal half and no self-compares
            # print("Comparing candycode %s with candycode %s" % (i1, i2))
            matches = len(list(set(s1).intersection(s2)))
            if matches > largest_shared_strings:
                largest_shared_strings = matches
print("Largest number of shared strings between any 2 candycodes: %i" % largest_shared_strings)
outfile = open(str(runs) + "_SUMMARY.txt", "a")
outfile.write("%i: Largest number of shared strings between any 2 candycodes: %i\n" % (repeat_id, largest_shared_strings))
outfile.close()



# # heatmap figure:
# # plt.figure()
# # plt.imshow(scores)
# # plt.savefig("HEATMAP.PDF")
# # plt.clf()

# print("\t\tmean\tmedian\tmin\tmax")

# # Diagonals:
# diags = []
# for i in range(runs):
#     diags.append(scores[i][i])
# print("diagonals:\t%0.3f\t%0.3f\t%0.3f\t%0.3f\t" %
#       (numpy.mean(diags), numpy.median(diags), numpy.min(diags), numpy.max(diags)))

# # Diagonals plus one half of others:
# others = []
# for i in range(runs):
#     for j in range(runs):
#         if i>=j:
#             others.append(scores[i][j])
# print("all others:\t%0.3f\t%0.3f\t%0.3f\t%0.3f\t" %
#       (numpy.mean(others), numpy.median(others), numpy.min(others), numpy.max(others)))

# # Histogram:
# score_dict = {}
# outfile = open(str(runs) + "_" + str(repeat_id) + ".txt", "w")
# for score in others:
#     try:
#         score_dict[score] = score_dict[score] + 1
#     except KeyError:
#         score_dict[score] = 1
# for key in sorted(score_dict.keys()):
#     print("%i\t%i" % (key, score_dict[key]))
#     outfile.write("%i\t%i\n" % (key, score_dict[key]))
# outfile.close()

# # Overall quality score:
# # print("120 Q:\t%0.3f" % (numpy.mean(diags) / numpy.mean(others)))




