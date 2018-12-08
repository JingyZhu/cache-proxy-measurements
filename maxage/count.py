import sys
import os
from urllib.parse import urlparse

total = 0
cachable = 0
cached = {}


web = sys.argv[1]
tmp = os.path.join('tmp', web)

rfile = open(tmp, 'r').read().split('\n')
while rfile[-1] == '':
    del rfile[-1]

for line in rfile:
    line = line.split('\t')
    if line[0] == '2' and int(line[2]) <= 24*60*60:
        cached[line[1]] = 0
    elif line[0] == '3' and int(line[2]) != 0:
        total += 1
        if line[1] in cached:
            cachable += 1

counts = os.path.join('counts', web)
cfile = open(counts, 'a')
if total != 0:
    cfile.write('all: {}\n'.format(str( cachable / total ) ) )
cfile.close()
# print('cachable: {}\ntotal: {}\nfraction: {}%'.format(cachable, total, cachable / total * 100))
