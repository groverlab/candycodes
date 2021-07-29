# (c) 2021 by William H. Grover  |  wgrover@engr.ucr.edu  |  groverlab.org

import sys
import subprocess

runs = 100000     # how many candycodes per simulation
repeats = 1    # how many simulations to perform in parallel

procs = []
for i in range(repeats):
    proc = subprocess.Popen([sys.executable, 'sim.py', str(runs), str(i)])
    procs.append(proc)

for proc in procs:
    proc.wait()
