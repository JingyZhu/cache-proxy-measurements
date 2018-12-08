"""
Get post req and post msg
"""
import json
import os

post_list = []

cacheable_list = os.listdir('../headers/cacheable')
uncacheable_list = os.listdir('../headers/uncacheable')
for cache_file in cacheable_list:
    cache_file = os.path.join('..', 'headers', 'cacheable', cache_file)
    file = open(cache_file, 'r', encoding='utf-8').read()
    cache_json = json.loads(file)
    for req in cache_json.values():
        if req['method'] != 'GET':
            req['filename'] = cache_file
            req['Cache'] = True
            try:
                req['postData'] = json.loads(req['postData'])
            except Exception as e:
                pass
            post_list.append(req)

for uncache_file in uncacheable_list:
    uncache_file = os.path.join('..', 'headers', 'uncacheable', uncache_file)
    file = open(uncache_file, 'r', encoding='utf-8').read()
    uncache_json = json.loads(file)
    for req in uncache_json.values():
        if req['method'] != 'GET':
            req['filename'] = cache_file
            req['Cache'] = False
            try:
                req['postData'] = json.loads(req['postData'])
            except Exception as e:
                print(str(e))
            post_list.append(req)

f = open('post_req.json', 'w+')
json.dump(post_list, f)