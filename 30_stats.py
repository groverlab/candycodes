# (c) 2021 by William H. Grover  |  wgrover@engr.ucr.edu  |  groverlab.org

f = open("120 library/03 picked text/030.txt", "r")
colors = {"D": 0, "G": 0, "L": 0, "O": 0, "P": 0, "R": 0, "W": 0, "Y": 0}
count = 0
for line in f:
	colors[line[0]] += 1
	count += 1
print("Code 30 has %i nonpareils" % count)
print(colors)
print("White is %f percent of all nonpareils" % (100 * colors["W"] / count))