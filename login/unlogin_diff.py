"""
Get all unlogin diff resources' req-resp pair
Output it in unlogin_diff.json
"""
import json
import os

compare_path = os.path.join('headers', 'compare')
meta_path = os.path.join('headers', 'meta')
unlogin_diff = {}
weblist = open('weblist', 'r').read().split('\n')
while weblist[-1] == "":
    del weblist[-1]

for web in weblist:
    unlogin_diff[web] = {}
    compare = open(os.path.join(compare_path, web.replace('/', '_') + '.json'))
    diff = json.load(compare)['diff']
    original = open(os.path.join(meta_path, web.replace('/', '_') + '.json'))
    meta = json.load(original)['available']
    for url, values in diff.items():
        for v in meta.values():
            if v['url'] == url:
                unlogin_diff[web][url] = v
                unlogin_diff[web][url]['diff'] = values
                break

f = open('unlogin_diff.json', 'w')
f.write(json.dumps(unlogin_diff))
f.close()