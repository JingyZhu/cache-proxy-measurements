import sys
import os
from urllib.parse import urlparse

cached = {}
req_url = {}
url_maxage = {}


web = sys.argv[1]
tmp = os.path.join('tmp', web)

rfile = open(tmp, 'r').read().split('\n')
while rfile[-1] == '':
    del rfile[-1]

for line in rfile:
    line = line.split('\t')
    if line[0] == '1':
        req_url[line[1]] = line[2]
    elif line[0] == '2':
        cached[line[1]] = int(line[2])
    elif line[0] == '3' and int(line[2]) != 0 and line[1] in cached:
        url = req_url[line[1]]
        url_maxage[url] = cached[line[1]]

maxfile = open('maxage_count', 'a')
for url, maxage in url_maxage.items():
    maxfile.write('{}\t{}\n'.format(url, maxage))
maxfile.close()