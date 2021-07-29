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
        for color in self.points:   # warning, doesn't yet exclude 'A'
            for x, y in self.points[color]:
                plt.text(x, y, 'R', horizontalalignment='center', verticalalignment='center')
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
    plt.plot(totals)
    min_theta = 0.0
    min_total = 99999999.99
    for theta, total in zip(numpy.linspace(0,2.0*3.1415926, bins), totals):
        if total < min_total:
            min_total = total
            min_theta = theta
    print("min_theta = %0.2f" % (min_theta) )
    return(min_theta)

c1 = candy()
with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter="\t")
    for color, x, y in csv_reader:
        c1.add(color, float(x), float(y))
c2 = candy()
with open(sys.argv[2]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter="\t")
    for color, x, y in csv_reader:
        c2.add(color, float(x), float(y))

c1.arrayify()
c2.arrayify()

c1.recenter()
c2.recenter()

# c1.plot_all()
# c2.plot_all()

min_theta = compare(c1, c2)

# c1.plot('W', min_theta, 'w')
# c2.plot('W', 0, 'b')

# c1.plot_all('w', min_theta)
# c2.plot_all('b', 0)

plt.show()