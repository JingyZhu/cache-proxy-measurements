"""
Generate random beref sequence
"""
import os
import random
import sys

MAX_SEQ = 1000
N = 100
filename = sys.argv[1]

beref = []

for i in range(N):
    num = random.randint(0, N-1)
    beref.append(sorted([1] + random.sample(range(2, MAX_SEQ+1), num)))

f = open(filename, 'w+')
for li in beref:
    f.write(' '.join([str(l) for l in li]) + '\n')
f.close()