"""
Count the fraction of method, headers for each cacheable and uncacheable request
"""
import os
import json
from urllib.parse import urlparse

cache_total_req = 0
uncache_total_req = 0
cache_guess_count = {}
uncache_guess_count = {}
cache_headers_count = {} # {'value': {'value': num}}
uncache_headers_count = {} # {'value': {'value': num}}

cache_headers_comp = {} # {'headers': [['values', frac]]}
uncache_headers_comp = {}

ignore_headers = ['cookie', ':path', ':authority', 'user-agent', 'referer', 'host']
def max(a, b):
    if a < b:
        return b
    return a

def guess(req, cache):
    # Get the type of url
    ext = req['type'] if req['type'] != '' else 'empty'
    # ext = os.path.splitext(urlparse(req['url']).path)[1]
    # ext = ext if ext != '' else 'empty'
    if cache:
        # CDN guess
        if 'cdn' in req['url']:
            if 'Contains cdn' not in cache_guess_count:
                cache_guess_count['Contains cdn'] = {'dummy':  0}
            cache_guess_count['Contains cdn']['dummy'] += 1
        # Assets
        if 'asset' in req['url']:
            if 'Contains assets' not in cache_guess_count:
                cache_guess_count['Contains assets'] = {'dummy':  0}
            cache_guess_count['Contains assets']['dummy'] += 1
        # method guess
        method = req['method']
        if method not in cache_guess_count:
            cache_guess_count[method] = {'dummy':  0}
        cache_guess_count[method]['dummy'] += 1
        if 'Resource: ' + ext not in cache_guess_count:
            cache_guess_count['Resource: ' + ext] = {'dummy': 0}
        cache_guess_count['Resource: ' + ext]['dummy'] += 1
        # Host is the same as referrer
        if 'headers' in req and 'referer' in req['headers']:
            # print('{} vs. {}'.format(urlparse(req['headers']['referer']).netloc, req['url']))
            if urlparse(req['headers']['referer']).netloc == urlparse(req['url']).netloc:
                if 'Host==Referer' not in cache_guess_count:
                    cache_guess_count['Host==Referer'] = {'dummy': 0}
                cache_guess_count['Host==Referer']['dummy'] += 1
        # See if Cookie and is a GET
        if 'headers' in req and 'cookie' in req['headers'] and method == "GET":
            if 'Cookie_Get' not in cache_guess_count:
                cache_guess_count['Cookie_Get'] = {'dummy': 0}
            cache_guess_count['Cookie_Get']['dummy'] += 1
        
        # Has query string and paramms
        if urlparse(req['url']).params != '':
            if 'Params' not in cache_guess_count:
                cache_guess_count['Params'] = {'dummy':  0}
            cache_guess_count['Params']['dummy'] += 1
        if urlparse(req['url']).query != '':
            if 'Params' not in cache_guess_count:
                cache_guess_count['Query'] = {'dummy':  0}
            cache_guess_count['Query']['dummy'] += 1
        # See proportion of data:
        if urlparse(req['url']).scheme == 'data':
            if 'Data' not in cache_guess_count:
                cache_guess_count['Data'] = {'dummy': 0}
            cache_guess_count['Data']['dummy'] += 1

    else:
        if 'cdn' in req['url']:
            if 'Contains cdn' not in uncache_guess_count:
                uncache_guess_count['Contains cdn'] = {'dummy':  0}
            uncache_guess_count['Contains cdn']['dummy'] += 1
        # Assets
        if 'asset' in req['url']:
            if 'Contains assets' not in uncache_guess_count:
                uncache_guess_count['Contains assets'] = {'dummy':  0}
            uncache_guess_count['Contains assets']['dummy'] += 1
        method = req['method']
        if method not in uncache_guess_count:
            uncache_guess_count[method] = {'dummy':  0}
        uncache_guess_count[method]['dummy'] += 1
        if 'Resource: ' + ext not in uncache_guess_count:
            uncache_guess_count['Resource: ' + ext] = {'dummy': 0}
        uncache_guess_count['Resource: ' + ext]['dummy'] += 1
        # Host is the same as referrer
        if 'headers' in req and 'referer' in req['headers']:
            # print('{} vs. {}'.format(urlparse(req['headers']['referer']).netloc, req['url']))
            if urlparse(req['headers']['referer']).netloc == urlparse(req['url']).netloc:
                if 'Host==Referer' not in uncache_guess_count:
                    uncache_guess_count['Host==Referer'] = {'dummy': 0}
                uncache_guess_count['Host==Referer']['dummy'] += 1

        # See if Cookie and is a GET
        if 'headers' in req and 'cookie' in req['headers'] and method == "GET":
            if 'Cookie_Get' not in uncache_guess_count:
                uncache_guess_count['Cookie_Get'] = {'dummy': 0}
            uncache_guess_count['Cookie_Get']['dummy'] += 1
        if urlparse(req['url']).params != '':
            if 'Params' not in uncache_guess_count:
                uncache_guess_count['Params'] = {'dummy':  0}
            uncache_guess_count['Params']['dummy'] += 1
        if urlparse(req['url']).query != '':
            if 'Params' not in uncache_guess_count:
                uncache_guess_count['Query'] = {'dummy':  0}
            uncache_guess_count['Query']['dummy'] += 1
        if urlparse(req['url']).scheme == 'data':
            if 'Data' not in uncache_guess_count:
                uncache_guess_count['Data'] = {'dummy': 0}
            uncache_guess_count['Data']['dummy'] += 1


def main():
    global cache_total_req
    global uncache_total_req
    global cache_guess_count
    global uncache_guess_count
    global cache_headers_count
    global uncache_headers_count
    cacheable_list = os.listdir('../headers/cacheable')
    uncacheable_list = os.listdir('../headers/uncacheable')
    for cache_file in cacheable_list:
        cache_file = os.path.join('..', 'headers', 'cacheable', cache_file)
        file = open(cache_file, 'r', encoding='utf-8').read()
        cache_json = json.loads(file)
        # print(cache_file)
        for reqId, req in cache_json.items():
            cache_total_req += 1
            headers = req.get('headers')
            if headers is not None:
                req['headers'] = {header.lower(): value for header, value in req['headers'].items()}
            guess(req, True)
            headers = req['headers'] if 'headers' in req else {}
            for header, value in headers.items():
                if header not in cache_headers_count:
                    cache_headers_count[header] = {}
                if value not in cache_headers_count[header]:
                    cache_headers_count[header][value] = 0
                cache_headers_count[header][value] += 1

    for uncache_file in uncacheable_list:
        uncache_file = os.path.join('..', 'headers', 'uncacheable', uncache_file)
        file = open(uncache_file, 'r', encoding='utf-8').read()
        uncache_json = json.loads(file)
        for reqId, req in uncache_json.items():
            uncache_total_req += 1
            headers = req.get('headers')
            if headers is not None:
                req['headers'] = {header.lower(): value for header, value in req['headers'].items()}
            guess(req, False)
            headers = req['headers'] if 'headers' in req else {}
            for header, value in headers.items():
                if header not in uncache_headers_count:
                    uncache_headers_count[header] = {}
                if value not in uncache_headers_count[header]:
                    uncache_headers_count[header][value] = 0
                uncache_headers_count[header][value] += 1

    # Get the largest comp of headers
    max_comp = 0
    for values in cache_headers_count.values():
        max_comp = max(max_comp, len(values.keys() ))
    for values in uncache_headers_count.values():
        max_comp = max(max_comp, len(values.keys() ))

    final_method = list(set().union(cache_guess_count.keys(), uncache_guess_count.keys()))
    final_headers = list(set().union(cache_headers_count.keys(), uncache_headers_count.keys()))

    bar_str = ""
    table_str = ""

    for method in final_method:
        cache_frac = 0 if method not in cache_guess_count else sum(cache_guess_count[method].values())
        uncache_frac = 0 if method not in uncache_guess_count else sum(uncache_guess_count[method].values())
        #if cache_frac/cache_total_req > 0.01 or uncache_frac/cache_total_req > 0.01:
        bar_str += "['{}', {}, {}],\n".format(method, cache_frac/cache_total_req, uncache_frac/uncache_total_req)

    for header in final_headers:
        cache_frac = 0 if header not in cache_headers_count else sum(cache_headers_count[header].values())
        uncache_frac = 0 if header not in uncache_headers_count else sum(uncache_headers_count[header].values())
        if cache_frac/cache_total_req > 0.01 or uncache_frac/cache_total_req > 0.01:
            bar_str += "['{}', {}, {}],\n".format(header, cache_frac/cache_total_req, uncache_frac / uncache_total_req)

        if header not in ignore_headers and (cache_frac / cache_total_req > 0.1 or uncache_frac / cache_total_req > 0.1):
            cache_headers_comp[header] = [[value, count / cache_frac] for value, count in cache_headers_count[header].items() ]
            uncache_headers_comp[header] = [[value, count / uncache_frac] for value, count in uncache_headers_count[header].items() ]

    # print('{} vs. {}'.format(cache_total_req, uncache_total_req))
    print(bar_str)
    cache_file = open('cache.json', 'w+')
    uncache_file = open('uncache.json', 'w+')
    json.dump(cache_headers_comp, cache_file)
    json.dump(uncache_headers_comp, uncache_file)

if __name__ == '__main__':
    main()