# (c) 2021 by William H. Grover  |  wgrover@engr.ucr.edu  |  groverlab.org

import matplotlib.pyplot as plt
import csv, sys, numpy, math

class candy:
    def __init__(self):
        self.points = {"A":[], "R":[], "P":[],  "O":[],  "Y":[],  "G":[],  "L":[],  "D":[],  "W":[] }
    def add(self, color, x, y):
        self.points['A'].append([x, y])
        self.points[color].append([x, y])
    def arrayify(self):
        for color in self.points:
            self.points[color] = numpy.array(self.points[color])
    def plot_all(self, color='gray', theta=0.0):
        for x,y in self.points['A']:
            x1, y1 = rot(x, y, theta)
            plt.plot(x1, y1, "o", color=color, markeredgecolor="k")
        # plt.plot(self.points['A'][:,0], self.points['A'][:,1], "o", color="gray", markeredgecolor="k")
    def plot_colors(self):
        for color in self.points:
            if color not in ['A']:
                for x, y in self.points[color]:
                    plt.text(x, y, color, horizontalalignment='center', verticalalignment='center')
    def plot(self, color, theta, markercolor="gray"):
        for x,y in self.points[color]:
            x1, y1 = rot(x, y, theta)
            plt.plot(x1, y1, "o", color=markercolor, markeredgecolor='k')  
    def plot_all_colors(self):
        for color in self.points:
            self.plot(color)
    def recenter(self):
        # recenter on 0,0:
        mean_x = numpy.mean(self.points['A'][:,0])
        mean_y = numpy.mean(self.points['A'][:,1])
        for color in self.points:
            self.points[color][:,0] = self.points[color][:,0] - mean_x
            self.points[color][:,1] = self.points[color][:,1] - mean_y
        # scale to +/- 1
        x_scale = (numpy.max(self.points['A'][:,0]) - numpy.min(self.points['A'][:,0])) / 2.0
        y_scale = (numpy.max(self.points['A'][:,1]) - numpy.min(self.points['A'][:,1])) / 2.0
        for color in self.points:
            self.points[color][:,0] = self.points[color][:,0] / x_scale
            self.points[color][:,1] = self.points[color][:,1] / y_scale  
        

def rot(x,y,theta):
    return [x * math.cos(theta) + y * math.sin(theta), -x * math.sin(theta) + y * math.cos(theta)]

def compare(candy1, candy2):
    bins = 100
    totals = numpy.zeros(bins)
    for color in candy1.points:
        if color in ['A']:
            print(color, len(candy1.points[color]), "(ignored)")
        else:
            print(color, len(candy1.points[color]))
            for theta, n in zip(numpy.linspace(0,2.0*3.1415926, bins), range(bins)):
                total = 0
                for x1,y1 in candy1.points[color]:
                    x1,y1 = rot(x1,y1,theta)  # rotate just the first candy?
                    min_distance = 9999999.99
                    for x2, y2 in candy2.points[color]:
                        dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                        if dist < min_distance:
                            min_distance = dist
                    total += min_distance
                totals[n] = totals[n] + total
    # plt.plot(totals)
    min_theta = 0.0
    min_total = 99999999.99
    for theta, total in zip(numpy.linspace(0,2.0*3.1415926, bins), totals):
        if total < min_total:
            min_total = total
            min_theta = theta
    print("min_total = %0.2f" % (min_total) )
    print("min_theta = %0.2f" % (min_theta) )
    return(min_total, min_theta)

candies = {}
for filename, candyID in zip(["1.1.txt", "1.2.txt", "1.3.txt", "1.4.txt", "1.5.txt", "1.6.txt", "1.7.txt", "1.8.txt", "1.9.txt",
                              "2.2.txt", "3.2.txt", "4.2.txt", "5.2.txt", "6.2.txt"],
                ["c11", "c12", "c13", "c14", "c15", "c16", "c17", "c18", "c19",
                        "c22", "c32", "c42", "c52", "c62"]):
    c = candy()
    print(filename)
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        for color, x, y in csv_reader:
            c.add(color, float(x), float(y))
    c.arrayify()
    c.recenter()
    candies[candyID] = c

for candy in ["c12", "c22", "c32", "c42", "c52", "c62"]:
    min_totals = []
    min_totals.append(compare(candies[candy], candies["c11"])[0])
    min_totals.append(compare(candies[candy], candies["c12"])[0])
    min_totals.append(compare(candies[candy], candies["c13"])[0])
    min_totals.append(compare(candies[candy], candies["c14"])[0])
    min_totals.append(compare(candies[candy], candies["c15"])[0])
    min_totals.append(compare(candies[candy], candies["c16"])[0])
    min_totals.append(compare(candies[candy], candies["c17"])[0])
    min_totals.append(compare(candies[candy], candies["c18"])[0])
    min_totals.append(compare(candies[candy], candies["c19"])[0])
    plt.plot(min_totals)


plt.show()

