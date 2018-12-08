"""
Test classifier for cacheable and uncacheable resources from the request
"""
import os
import json
from urllib.parse import urlparse
from decimal import Decimal
from statistics import median
from sklearn import metrics
from common import *

cache_total_req = [0, 0]
uncache_total_req = [0, 0]
cache_hit =[0, 0]
cache_miss = [0, 0]
uncache_hit = [0, 0]
uncache_miss = [0, 0]
cache_guess = [0, 0]
uncache_guess = [0, 0]
first_guess = 0

avg_size = [[], []]


# CM measurements
y_pred = []
y_true = []


def max(a, b):
    if a < b:
        return b
    return a

def guess(req, cache, byte):
    global cache_hit
    global cache_miss
    global uncache_hit
    global uncache_miss
    global cache_guess
    global uncache_guess
    global first_guess
    global avg_size

    global y_test
    global y_true

    cacheable = None
    ext = os.path.splitext(urlparse(req['url']).path)[1]
    ext = ext.lower()

    if req['method'] != 'GET':
        cacheable = False
    elif urlparse(req['url']).query != '':
        cacheable = False
    elif 'cdn' in req['url'] or 'asset' in req['url']:
        cacheable = True
    elif ext in cacheable_ext:
        cacheable = True
    elif req['type'] == 'Font':
        cacheable = True
    # elif 'headers' in req and 'referer' in req['headers'] and urlparse(req['url']).netloc == urlparse(req['headers']['referer']).netloc:
        # cacheable = True
    # uncacheable
    if cacheable is None:
        if req['type'] == 'XHR' or req['type'] == 'Document':
            cacheable = False
        elif ext in uncacheable_ext:
            cacheable = False
        elif 'headers' in req:
            if 'content-type' in req['headers'] or 'content-length' in req['headers'] or 'cookie' in req['headers']:
                cacheable = False
        cacheable = True if cacheable is None else cacheable
    
    if cache:
        if cacheable == cache:
            cache_hit[0] += 1
            cache_hit[1] += byte
            y_pred.append(1)
        else:
            cache_miss[0] += 1
            cache_miss[1] += byte
            y_pred.append(-1)
        y_true.append(1)
    else:
        if cacheable == cache:
            uncache_hit[0] += 1
            uncache_hit[1] += byte
            avg_size[0].append(byte)
            y_pred.append(-1)
        else:
            uncache_miss[0] += 1
            uncache_miss[1] += byte
            avg_size[1].append(byte)
            y_pred.append(1)
        y_true.append(-1)
    if cacheable:
        cache_guess[0] += 1
        cache_guess[1] += byte
    else:
        uncache_guess[0] += 1
        uncache_guess[1] += byte



def main():
    global cache_total_req
    global uncache_total_req
    global cache_hit
    global cache_miss
    global uncache_hit
    global uncache_miss
    global first_guess
    global avg_size

    global y_true
    global y_pred

    cacheable_list = os.listdir('../headers/cacheable')
    uncacheable_list = os.listdir('../headers/uncacheable')
    for cache_file in cacheable_list:
        cache_file = os.path.join('..', 'headers', 'cacheable', cache_file)
        file = open(cache_file, 'r', encoding='utf-8').read()
        cache_json = json.loads(file)
        # print(cache_file)
        for req in cache_json.values():
            byte = req['bytes'] if 'bytes' in req else 0
            cache_total_req[0] += 1
            cache_total_req[1] += byte
            guess(req, True, byte)

    for uncache_file in uncacheable_list:
        uncache_file = os.path.join('..', 'headers', 'uncacheable', uncache_file)
        file = open(uncache_file, 'r', encoding='utf-8').read()
        uncache_json = json.loads(file)
        for req in uncache_json.values():
            byte = req['bytes'] if 'bytes' in req else 0
            uncache_total_req[0] += 1
            uncache_total_req[1] += byte
            guess(req, False, byte)

    # print("""
    #     Counts: \n
    #     Cache / Uncache guess: {} / {} \n
    #     Total cache: {} \n
    #     Hit / Miss : {} / {} \n
    #     Rate: {} \n
    #     Total uncache: {} \n
    #     Hit / Miss : {} / {} \n
    #     Rate: {} 
    # """.format(cache_guess[0], uncache_guess[0],
    #             cache_total_req[0], cache_hit[0], cache_miss[0], cache_hit[0] / cache_total_req[0], 
    #             uncache_total_req[0], uncache_hit[0], uncache_miss[0], uncache_hit[0] / uncache_total_req[0]))
    print("""
        Bytes: \n
        Cache / Uncache guess: {:.2E} / {:.2E} \n
        Total cache: {:.2E} \n
        Hit / Miss : {:.2E} / {:.2E} \n
        Rate: {} \n
        Total uncache: {:.2E} \n
        Hit / Miss : {:.2E} / {:.2E} \n
        Rate: {} 
    """.format(Decimal(cache_guess[1]), Decimal(uncache_guess[1]),
                Decimal(cache_total_req[1]), Decimal(cache_hit[1]), Decimal(cache_miss[1]), cache_hit[1] / cache_total_req[1], 
                Decimal(uncache_total_req[1]), Decimal(uncache_hit[1]), Decimal(uncache_miss[1]), uncache_hit[1] / uncache_total_req[1]))
    print("size: {}/ {}".format(median(avg_size[0]), median(avg_size[1])))
    print('AUROC: ', metrics.roc_auc_score(y_true, y_pred))
    print(metrics.confusion_matrix(y_true, y_pred))

if __name__ == '__main__':
    main()