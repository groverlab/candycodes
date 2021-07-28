import math

p = 0.01
n = math.sqrt(2 * 2**122 * math.log(1 / (1-p)))
print("%G random UUIDs have a collision probability of %f" % (n, p))
# # world population is 7.9 billion, 7.9x10^9
codes_per_person = n / 7.9e9
print("{:,} codes per person on Earth".format(int(codes_per_person)))