import math
import os
from statistics import median
from subprocess import *
import random

bfiles = os.listdir('bytes')
cfiles = os.listdir('counts')
bfracs = []
cfracs = []
bcstr = ''

def parse_portion(filename):
    frac = []
    data = open(filename, 'r').read().split('\n')
    while data[-1] == '':
        del data[-1]
    # print(filename + " " + str(len(data)))
    for datus in data:
        try:
            datus = datus.split(' ')
            frac.append(float(datus[1]))
        except Exception as e:
            pass
    frac.sort()
    return None if frac == [] else median(frac)


for bfile in bfiles:
    f = open(os.path.join('bytes', bfile), 'r').read()
    if f == '':
        os.remove(os.path.join('bytes',bfile))
        continue

for cfile in cfiles:
    f = open(os.path.join('counts', cfile), 'r').read()
    if f == '':
        os.remove(os.path.join('counts',cfile))
        continue

bfiles = os.listdir('bytes')
cfiles = os.listdir('counts')

for bfile in bfiles:
    frac = parse_portion(os.path.join('bytes',bfile))
    if frac != None:
        bfracs.append(frac)


for cfile in cfiles:
    frac = parse_portion(os.path.join('counts',cfile))
    if frac != None:
        cfracs.append(frac)

bfracs.sort()
cfracs.sort()

i = 1
for bfrac in bfracs:
    bcstr += '[{}, {}, null],\n'.format( bfrac, i / len(bfracs) )
    i += 1


i = 1
for cfrac in cfracs:
    bcstr += '[{}, null, {}],\n'.format( cfrac, i / len(cfracs) )
    i += 1


analyze_file = open('analyze_str', 'w+')
analyze_file.write(bcstr)
analyze_file.close()


url_maxage = {}
maxfile = open('maxage_count', 'r').readlines()
for line in maxfile:
    line = line.strip().split('\t')
    url_maxage[line[0]] = int(line[1])

maxage_list = sorted(list(url_maxage.values()))
maxstr, i, size= '', 1, len(maxage_list)

for value in maxage_list:
    maxstr += '[{}, {}],\n'.format(value, i/size)
    i += 1

maxage_file = open('maxage_str', 'w+')
maxage_file.write(maxstr)
maxage_file.close()
