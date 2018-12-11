#!/anaconda3/bin/python3
"""
Load certain page with multiple times
Fetch one with median #resources
Union the same-length response with login cookie 
CDP ways and python requests way
"""
import os
from shutil import copyfile
import sys
import json
from subprocess import *
import requests
import common
from hyper.contrib import HTTP20Adapter
from urllib.parse import urlparse
from statistics import median
from extr_resource import extr_resource

if __name__ == '__main__':
    host = sys.argv[1]
    url = 'https://' + host
    cookie_dict = {}

def union():
    """Use Chromium to individually load the resources"""
    unioned_dict = {'available': {}, "unavailable": {}, 'cookie_count': cookie_dict}
    f = open(os.path.join('headers', 'login',  host.replace('/', '_') + '.json'), 'r').read()
    login_json = json.loads(f)
    unioned_dict['unavailable'] = login_json['unavailable']
    call(['node', 'load.js', host])
    f = open(os.path.join('headers', 'compare',  host.replace('/', '_') + '.json'), 'r').read()
    compare_json = json.loads(f)

    for k, v in login_json['available'].items():
        if v['url'] in compare_json['same']:
            unioned_dict['available'][k] = v
        elif v['url'] in compare_json['diff']:
            url = v['url']
            unioned_dict['unavailable'][k] = v
            unioned_dict['unavailable'][k]['headers'] = [compare_json['diff'][url]['headers'], v['headers']]
            unioned_dict['unavailable'][k]['length'] = [compare_json['diff'][url]['length'][0], v['length']]

    f = open(os.path.join('headers', 'login', host.replace('/', '_') + '.json'), 'w+')
    f.write(json.dumps(unioned_dict))
    f.close()
    os.remove(os.path.join('headers', 'compare', host.replace('/', '_') + '.json'))
    return (len(unioned_dict['available'].keys()), len(unioned_dict['unavailable'].keys()))



def load(login):
    compare = {'same': {}, 'diff': {}}
    for _, req in login.items():
        if "length" not in req:
            continue
        if req.get('method') == 'GET' and 'headers' in req and ('cookie' in req['headers'] or 'Cookie' in req['headers']):
            try:
                # s = requests.Session()
                # s.mount('https://' + urlparse(req['url']).netloc, HTTP20Adapter())
                # r = s.get(req['url'], headers=req['headers'], timeout=5)
                headers = common.strip_colon(req['headers'])
                r = requests.get(req['url'], headers=headers, timeout=5)
            except Exception as e:
                print(str(e))
                continue
            byte, text = common.find_length(r, True)
            is_similar, similarity = common.similar(byte, req['length'], text, extr_resource(host.replace('/', '_'), req['url']))
            if is_similar:
                compare['same'][req['url']] = [byte]
            else:
                compare['diff'][req['url']] = [byte, req['length'], similarity]
    f = open(os.path.join('headers', 'compare', host.replace('/', '_') + '.json'), 'w+')
    f.write(json.dumps(compare))
    f.close()
        

def union_requests(host):
    """Fetch resources through requests"""
    unioned_dict = {'available': {}, "unavailable": {}, 'cookie_count': cookie_dict}
    f = open(os.path.join('headers', 'login', host.replace('/', '_') + '.json'), 'r').read()
    login_json = json.loads(f)
    unioned_dict['unavailable'] = login_json['unavailable']
    load(login_json['available'])
    f = open(os.path.join('headers', 'compare', host.replace('/', '_') + '.json'), 'r').read()
    compare_json = json.loads(f)

    for k, v in login_json['available'].items():
        if 'length' not in v:
            continue
        if v['url'] in compare_json['same']:
            unioned_dict['available'][k] = v
        elif v['url'] in compare_json['diff']:
            url = v['url']
            unioned_dict['unavailable'][k] = v
            unioned_dict['unavailable'][k]['length'] = [compare_json['diff'][url][0], v['length'], compare_json['diff'][url][2]]

    f = open(os.path.join('headers', 'login', host.replace('/', '_') + '.json'), 'w+')
    f.write(json.dumps(unioned_dict))
    f.close()
    os.remove(os.path.join('headers', 'compare', host.replace('/', '_') + '.json'))
    return (len(unioned_dict['available'].keys()), len(unioned_dict['unavailable'].keys()))


def multiple_loads(num_loads, url):
    host = urlparse(url).netloc + urlparse(url).path
    hostfilename = host.replace('/', '_')
    num_resources = []
    meta_path = os.path.join('headers', 'meta')
    resource_path = os.path.join('headers', 'resources')
    for i in range(num_loads):
        call(['node', 'run.js', url, str(i)])
    for i in range(num_loads):
        f = open(os.path.join(meta_path, '{}.{}.json'.format(hostfilename, i) ))
        j = json.load(f)
        num_resources.append(len(j['available'].keys()))
    print("num_resources: ", num_resources)
    index = num_resources.index(median(num_resources))
    os.rename(os.path.join(meta_path, '{}.{}.json'.format(hostfilename, index)), \
                os.path.join(meta_path, '{}.json'.format(hostfilename)))
    os.rename(os.path.join(resource_path, '{}.{}.json'.format(hostfilename, index)), \
                os.path.join(resource_path, '{}.json'.format(hostfilename)))
    for i in range(num_loads):
        if i != index:
            os.remove(os.path.join(meta_path, '{}.{}.json'.format(hostfilename, i)))
            os.remove(os.path.join(resource_path, '{}.{}.json'.format(hostfilename, i)))


def main():
    global cookie_dict
    if len(sys.argv) > 2 and sys.argv[2] == 'new':
        if host + '.json' in os.listdir(os.path.join('headers', 'login')): 
            try:
                os.remove(os.path.join('headers', 'meta', host + '.json'))
            except:
                pass
        multiple_loads(3, url)
    copyfile(os.path.join('headers', 'meta', host.replace('/', '_') + '.json'), os.path.join('headers', 'login', host.replace('/', '_') + '.json'))
    cookie_dict = eval(check_output(['python3', 'count_cookie_domain.py', host]))
    old, new = 0, (-1, -1)
    while new[0] != old:
        old = new[0]
        new = union_requests(host)
        print(new)

if __name__ == '__main__':
    main()