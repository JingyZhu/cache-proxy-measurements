"""
Measure the number of requests for cache/uncache resources
"""
import json
import os
import common

cache_req_num = []
uncache_req_num = []

cacheable_list = os.listdir('../headers/cacheable')
uncacheable_list = os.listdir('../headers/uncacheable')
for cache_file in cacheable_list:
    cache_file = os.path.join('..', 'headers', 'cacheable', cache_file)
    file = open(cache_file, 'r', encoding='utf-8').read()
    cache_json = json.loads(file)
    for req in cache_json.values():
        if 'headers' in req:
            cache_req_num.append(len(req['headers']))
        else:
            cache_req_num.append(0)

for uncache_file in uncacheable_list:
    uncache_file = os.path.join('..', 'headers', 'uncacheable', uncache_file)
    file = open(uncache_file, 'r', encoding='utf-8').read()
    uncache_json = json.loads(file)
    for req in uncache_json.values():
        if 'headers' in req:
            uncache_req_num.append(len(req['headers']))
        else:
            uncache_req_num.append(0)
        
common.gen_cdf([cache_req_num, uncache_req_num], 'num_request.log')