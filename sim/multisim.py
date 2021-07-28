import sys
import subprocess

runs = 30000     # how many candycodes per simulation
repeats = 4    # how many simulations to perform in parallel

procs = []
for i in range(repeats):
    proc = subprocess.Popen([sys.executable, 'sim.py', str(runs), str(i)])
    procs.append(proc)

for proc in procs:
    proc.wait()
