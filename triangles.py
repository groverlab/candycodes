import matplotlib.pyplot as plt
import csv, sys, math, scipy.spatial, os
import numpy as np
from collections import Counter
plt.rcParams["font.family"] = "Helvetica"

outfile = open("REPORT.TXT", 'w')

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


# moving this out here to avoid memory problems
fig, ax = plt.subplots(figsize=(4,4))



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

    def __init__(self, filename):
        self.id = os.path.split(filename)[1][:-4]
        candy_id = 0
        self.number_of_candies = 0
        self.candies = []
        self.strings = []
        self.filename = filename
        f = open(self.filename)
        for color, x, y in csv.reader(f, delimiter="\t"):
            self.candies.append(candy(candy_id, color, float(x), -float(y)))
            candy_id += 1
            self.number_of_candies += 1
            
    def triangulate(self):
        """Method for converting the candycode to its string representation."""
        global total_good_codes, total_discards_on_edge, total_discards_too_few_colors
        print("\u001b[33m%s:\u001b[0m\n" % self.filename)
        good_codes = 0
        discards_too_few_colors = 0
        discards_on_edge = 0
        self.tri = scipy.spatial.Delaunay([[c.x, c.y] for c in self.candies])
        for center in self.candies:
            on_edge = False
            too_few_colors = False
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
            for n in center.neighbors:
                print("      %i: %s (%0.1f %0.1f) %0.1f" % (n.id, n.color, n.x, n.y, n.theta))
            code_string = center.color + ''.join([n.color for n in center.neighbors])
            # NEW:  saving the string with the candy regardless of whether it is a good string,
            # for use in figures later on.  This used to be in the "else" statement below.
            center.string = code_string  # save the string with the candy too
            if len(set(code_string)) < min_colors:
                too_few_colors = True
            if on_edge and remove_edges:
                print("\u001b[31m      Discarded because on edge\033[0m\n")
                discards_on_edge += 1
                total_discards_on_edge += 1
                center.discarded_because_on_edge = True
            elif too_few_colors:
                print("\u001b[31m      Discarded because too few colors\033[0m\n")
                discards_too_few_colors += 1
                total_discards_too_few_colors += 1
                center.discarded_because_too_few_colors = True
            else:
                self.strings.append(code_string)
                print("\u001b[32m      Good code\033[0m\n")
                good_codes += 1
                total_good_codes += 1
        if remove_duplicates:
            self.strings = list(set(self.strings))  # remove duplicates
        self.strings.sort()
        print("   Good codes:", end="")
        for s in self.strings:
            print(" %s" % s, end="")
        print()
        outfile.write("%s: %i good codes, %i disc on edge, %i disc too few colors\n" % 
                      (self.filename, good_codes, discards_on_edge, discards_too_few_colors))

        
        
        # Individual candy plots:

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
            # Actually, plot all strings so that we can show discards too:
            # if not c.discarded_because_too_few_colors and not c.discarded_because_too_few_colors:
            if True:
                plt.text(c.x, c.y-0.03*span, c.string, color="k",
                         horizontalalignment='center', verticalalignment='center',
                         fontsize=5)

        # add candy ID to lower-right corner:
        plt.text(0.9, 0.1, self.id, horizontalalignment="center", verticalalignment="center",
                 transform = ax.transAxes)
            
        plt.savefig("120 library/04 candy plots/" + str(self.id) + ".PDF")
        plt.clf()






files = []

for f in os.listdir("120 library/03 picked text"):
    if f.endswith(".txt"):
        files.append(os.path.join("120 Library/03 picked text", f))
files.sort()


# Convert the candycodes to strings:
candycodes = []
for f in files:
    c = candycode(f)
    c.triangulate()
    candycodes.append(c)

# Write to the report file:
outfile.write("TOTALS:\n" +
      "   %i good codes\n" % total_good_codes +
      "   %i discards because on edge\n" % total_discards_on_edge +
      "   %i discards because too few colors\n" % total_discards_too_few_colors)






# Candycode string statistics

candycode_string_lengths = []
for c in candycodes:
    if "med" not in c.id:  # don't include pre-med and post-med copies of candycodes
        candycode_string_lengths.append(len(c.strings))
outfile.write("\n")
outfile.write("Candycode string statistics:\n")
outfile.write("Avg number of strings per candycode:  %f\n" % np.mean(candycode_string_lengths))
outfile.write("Med number of strings per candycode:  %f\n" % np.median(candycode_string_lengths))
outfile.write("Min number of strings per candycode:  %f\n" % np.min(candycode_string_lengths))
outfile.write("Max number of strings per candycode:  %f\n" % np.max(candycode_string_lengths))






scores = np.zeros((len(candycodes), len(candycodes)))
for i1, c1 in enumerate(candycodes):
    for i2, c2 in enumerate(candycodes):
        print("%s\t%s" % (c1.filename, c2.filename))
        matches = 0
        for s1 in c1.strings:
            for s2 in c2.strings:
                if s1 == s2:
                    matches += 1
                    print("\u001b[32m   Match: %s\033[0m" % s1)
        scores[i1][i2] = matches
        print("      Score: %i\n" % matches)


# # heatmap figure:
# plt.figure()
# plt.imshow(scores)
# plt.savefig("HEATMAP.PDF")
# plt.clf()









outfile.write("\n\n####### 120 DIAGONALS:\n")

# Diagonals:
diags = []
for i in range(120):
    diags.append(scores[i][i])
outfile.write("%0.3f\t%0.3f\t%0.3f\t%0.3f\t\n\n" %
      (np.mean(diags), np.median(diags), np.min(diags), np.max(diags)))

# Histogram:
score_dict = {}
for score in diags:
    try:
        score_dict[score] = score_dict[score] + 1
    except KeyError:
        score_dict[score] = 1
for key in sorted(score_dict.keys()):
    print("%i\t%i" % (key, score_dict[key]))
    outfile.write("%i\t%i\n" % (key, score_dict[key]))








outfile.write("\n\n####### 120 HALF NON-DIAGONALS:\n")

others = []
for i in range(120):
    for j in range(120):
        if i>j:
            others.append(scores[i][j])
outfile.write("%0.3f\t%0.3f\t%0.3f\t%0.3f\t\n\n" %
      (np.mean(others), np.median(others), np.min(others), np.max(others)))

# Histogram:
score_dict = {}
for score in others:
    try:
        score_dict[score] = score_dict[score] + 1
    except KeyError:
        score_dict[score] = 1
for key in sorted(score_dict.keys()):
    print("%i\t%i" % (key, score_dict[key]))
    outfile.write("%i\t%i\n" % (key, score_dict[key]))









outfile.write("\n\n####### 120 DIAGONALS PLUS HALF NON-DIAGONALS:\n")

others = []
for i in range(120):
    for j in range(120):
        if i>=j:
            others.append(scores[i][j])
outfile.write("%0.3f\t%0.3f\t%0.3f\t%0.3f\t\n\n" %
      (np.mean(others), np.median(others), np.min(others), np.max(others)))

# Histogram:
score_dict = {}
for score in others:
    try:
        score_dict[score] = score_dict[score] + 1
    except KeyError:
        score_dict[score] = 1
for key in sorted(score_dict.keys()):
    print("%i\t%i" % (key, score_dict[key]))
    outfile.write("%i\t%i\n" % (key, score_dict[key]))








outfile.write("\n\n####### PRE-MED AND POST-MED VS 120:\n")

match_scores = []

# pre-med1 vs. 120:
pre_med1 = scores[123][0:120]
outfile.write("pre-med1 vs 120:  " + str(list(zip(Counter(pre_med1).keys(), Counter(pre_med1).values()))) + "\n")
match_scores.append(max(pre_med1))

# post-med1 vs. 120:
post_med1 = scores[120][0:120]
outfile.write("post_med1 vs 120: " + str(list(zip(Counter(post_med1).keys(), Counter(post_med1).values()))) + "\n")
match_scores.append(max(post_med1))

# pre-med2 vs. 120:
pre_med2 = scores[124][0:120]
outfile.write("pre-med2 vs 120:  " + str(list(zip(Counter(pre_med2).keys(), Counter(pre_med2).values()))) + "\n")
match_scores.append(max(pre_med2))

# post-med2 vs. 120:
post_med2 = scores[121][0:120]
outfile.write("post_med2 vs 120: " + str(list(zip(Counter(post_med2).keys(), Counter(post_med2).values()))) + "\n")
match_scores.append(max(post_med2))

# pre-med3 vs. 120:
pre_med3 = scores[125][0:120]
outfile.write("pre-med3 vs 120:  " + str(list(zip(Counter(pre_med3).keys(), Counter(pre_med3).values()))) + "\n")
match_scores.append(max(pre_med3))

# post-med3 vs. 120:
post_med3 = scores[122][0:120]
outfile.write("post_med3 vs 120: " + str(list(zip(Counter(post_med3).keys(), Counter(post_med3).values()))) + "\n")
match_scores.append(max(post_med3))

outfile.write("\n\nSUMMARY OF SIX MATCH SCORES:\n")
outfile.write("  avg: %f\n" % np.mean(match_scores))
outfile.write("  std: %f\n" % np.std(match_scores))
outfile.write("  max: %f\n" % np.max(match_scores))
outfile.write("  min: %f\n" % np.min(match_scores))






# basic candycode color statistics
numbers_of_candies = []
colors = {"R":0, "P":0, "O":0, "Y":0, "G":0, "L":0, "D":0, "W":0 }
nonwhites = 0

for c in candycodes:
    if "med" not in c.id:  # don't include pre-med and post-med copies of candycodes
        print("%s: %i" % (c.id, c.number_of_candies))
        numbers_of_candies.append(c.number_of_candies)
        for cc in c.candies:
            colors[cc.color] = colors[cc.color] + 1
            if "W" not in cc.color:
                nonwhites += 1

outfile.write("\n\n\n")
numbers_of_candies = np.array(numbers_of_candies)
outfile.write("Number of candycodes: %i\n" % len(numbers_of_candies))
outfile.write("Mean number of candies per candycode: %f\n" % np.mean(numbers_of_candies))
outfile.write("Median number of candies per candycode: %f\n" % np.median(numbers_of_candies))
outfile.write("Max number of candies per candycode: %f\n" % np.max(numbers_of_candies))
outfile.write("Min number of candies per candycode: %f\n" % np.min(numbers_of_candies))
for key, value in colors.items():
    outfile.write("%s: %i\n" % (key, value))
outfile.write("Average number of non-white candies: %f\n" % (nonwhites / 7.0))
outfile.write("White excess factor: %f\n" % (colors["W"] / (nonwhites / 7.0)))







# commercial 8 pie chart:
fig1, ax1 = plt.subplots(figsize=(3,2.5))
wedges, texts, autotexts = ax1.pie(colors.values(), autopct='%1.1f%%', pctdistance=0.8, 
    labels=("Red", "Pink", "Orange", "Yellow", "Light green", "Light blue", "Dark blue", "White"),
    colors=("red", "pink", "orange", "yellow", "lightgreen", "lightblue", "dodgerblue", "white"))
for w in wedges:
    w.set_linewidth(2)
    w.set_edgecolor('black')
# ax1.axis('equal')
# texts[0].set_fontsize(4)
fig1.savefig("color_pie_8_commercial.pdf")


# equal 8 pie chart:
figA, axA = plt.subplots(figsize=(3,2.5))
wedges, texts, autotexts = axA.pie([1,1,1,1,1,1,1,1], autopct='%1.1f%%', pctdistance=0.8,
    labels=("Red", "Pink", "Orange", "Yellow", "Green", "Light blue", "Dark blue", "White"),
    colors=("red", "pink", "orange", "yellow", "lightgreen", "lightblue", "dodgerblue", "white"))
for w in wedges:
    w.set_linewidth(2)
    w.set_edgecolor('black')
# axA.axis('equal')
figA.savefig("color_pie_8_equal.pdf")


# equal 15 pie chart:
figB, axB = plt.subplots(figsize=(3,2.5))
wedges, texts, autotexts = axB.pie([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], autopct='%1.1f%%', pctdistance=0.8,
    labels=("Red", "Pink", "Orange", "Yellow", "Green", "Light blue", "Dark blue", "White",
            "Light gray", "Dark gray", "Black", "Dark green", "Magenta", "Purple", "Brown"),
    colors=("red", "pink", "orange", "yellow", "lightgreen", "lightblue", "dodgerblue", "white",
            "silver", "dimgray", "black", "darkgreen", "magenta", "purple", "sienna"))
autotexts[9].set_color('white')
autotexts[10].set_color('white')
autotexts[11].set_color('white')
autotexts[12].set_color('white')
autotexts[13].set_color('white')
autotexts[14].set_color('white')
for w in wedges:
    w.set_linewidth(2)
    w.set_edgecolor('black')
# axB.axis('equal')
figB.savefig("color_pie_15_equal.pdf")






