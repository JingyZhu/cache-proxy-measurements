"""
Randomly sample some cacheable/uncacheable json
"""
import os
import json
import random
import sys
from urllib.parse import urlparse

sample_size = 5
mode = 'cacheable'
cacheable = {}
uncacheable = {}
dir_list = os.listdir('headers/{}'.format(mode))
files = random.sample(dir_list, 5)

for file in files:
    del_dict = []
    j1 = json.loads(open('headers/cacheable/{}'.format(file) , 'r', encoding='utf-8').read())
    for k, v in j1.items():
        if urlparse(v['url']).scheme == 'data' or v['method'] != 'GET':
            del_dict.append(k)
    for k in del_dict:
        del j1[k]
    cacheable[file] = j1
    del_dict = []
    j2 = json.loads(open('headers/uncacheable/{}'.format(file) , 'r', encoding='utf-8').read())
    for k, v in j2.items():
        if urlparse(v['url']).scheme == 'data' or v['method'] != 'GET':
            del_dict.append(k)
    for k in del_dict:
        del j2[k]
    uncacheable[file] = j2


w1 = open('cache.json', 'w+')
w2 = open('uncache.json', 'w+')
w1.write(json.dumps(cacheable))
w2.write(json.dumps(uncacheable))