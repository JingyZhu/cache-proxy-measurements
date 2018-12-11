"""
Count the number of login diff, login/unlogin same, login/unlogin diff, no cookies
"""
import os
import json
import csv
from urllib.parse import urlparse

file_list = open('weblist', 'r').read().split()
while file_list[-1] == '':
    del file_list[-1]

types = ['Document', 'Image', 'Script', 'Fetch', 'XHR', 'Stylesheet']
# fb_j = json.loads(open('headers/login/facebook.com.json', 'r').read())['cookie_count']
# netflix_j = json.loads(open('headers/login/netflix.com.json', 'r').read())['cookie_count']
# with open('cookie2.csv', 'w') as f:
#     w = csv.writer(f)
#     for tup in netflix_j.items():
#         w.writerow(tup)

def count_cookie(cookie_dict):
    cok,tot = 0, 0
    for value  in cookie_dict.values():
        cok += value[0]
        tot += value[1]
    return cok, tot

def find_bytes(meta, url):
    for _, v in meta.items():
        if v['url'] == url:
            return v['bytes']

def original_count():
    """
    Count for diff resources counts
    """
    strr = ''
    for file in file_list:
        f1 = open(os.path.join('headers/compare', file.replace('/', '_') + '.json'), 'r').read()
        j1 = json.loads(f1)
        f2 = open(os.path.join('headers/login', file.replace('/', '_') + '.json'), 'r').read()
        j2 = json.loads(f2)
        same = len(j1['same'].keys())
        diff = len(j1['diff'].keys())
        unavailable = len(j2['unavailable'].keys())
        cok, tot = count_cookie(j2['cookie_count'])
        strr += "['{}', {}, {}, {}, {}], \n".format(file, unavailable, diff, same, tot-cok)
    print(strr)

def original_count_bytes():
    """
    Count for diff resources counts in bytes
    """
    strr = ''
    for file in file_list:
        f1 = open(os.path.join('headers/compare', file.replace('/', '_') + '.json'), 'r').read()
        j1 = json.loads(f1)
        f2 = open(os.path.join('headers/login', file.replace('/', '_') + '.json'), 'r').read()
        j2 = json.loads(f2)
        f3 = open(os.path.join('headers/meta', file.replace('/', '_') + '.json'), 'r').read()
        j3 = json.loads(f3)['available']
        same, diff, unavailable = 0, 0, 0
        remain = 0
        urls = {}
        for k in j1['same'].keys():
            urls[k] = 0
            same += find_bytes(j3, k)
        for k in j1['diff'].keys():
            urls[k] = 0
            diff += find_bytes(j3, k)
        for v in j2['unavailable'].values():
            urls[v['url']] = 0
            unavailable += find_bytes(j3, v['url'])
        for v in j3.values():
            if v['url'] not in urls and 'bytes' in v:
                urls[v['url']] = 0;
                remain += v['bytes']
        strr += "['{}', {}, {}, {}, {}], \n".format(file, unavailable/1000, diff/1000, same/1000, remain/1000)
    print(strr)



def conditions(v):
    key_words = ['ajax', 'api']
    rval1, rval2 = True, True
    no_init = v.get('initiator') == None or v.get('initiator') == "nothing"
    initiator_ext = '' if no_init else os.path.splitext(urlparse(v['initiator']).path)[1]
    query = urlparse(v['url']).query != ''
    rval1 = no_init and v['type'] == 'Document'
    rval2 = query and (v.get('type') in ['XHR', 'Fetch'])
    rval3 = (v.get('type') in ['XHR', 'Fetch']) and any([w in v['url'] for w in key_words])
    # rval2 = rval2 and any([w in v['url'] for w in key_words])
    return rval1 or rval2 or rval3


def initiator_count():
    init = {'nothing_biased':0, 'something': 0}
    for file in file_list:
        f2 = open(os.path.join('headers/login', file.replace('/', '_') + '.json'), 'r').read()
        j2 = json.loads(f2)
        for v in j2['available'].values():
            if conditions(v):
                init['nothing_biased'] += 1
            else:
                init['something'] += 1
        for v in j2['unavailable'].values():
            if conditions(v):
                init['nothing_biased'] += 1
            else:
                init['something'] += 1
    print(init)

def unlogin_type_count():
    intend = {'intend':0, 'else': 0}
    f = open('unlogin_diff.json').read()
    j = json.loads(f)
    for web in j.values():
        for v in web.values():
            if conditions(v):
                intend['intend'] += 1
            else:
                intend['else'] += 1
    print(intend)


    # diff_type = {}
    # #  Unavailable
    # for v in j2['unavailable'].values():
    #     if v['type'] not in diff_type:
    #         diff_type[v['type']] = 0
    #     diff_type[v['type']] += 1
    # for v in j1['diff'].values():
    #     if v[2] not in diff_type:
    #         diff_type[v[2]] = 0
    #     diff_type[v[2]] += 1
    
    # for k in diff_type.keys():
    #     assert(k in types)
    # strr2 += "['{}', {}], \n".format(file, ','.join([str(diff_type[t]) if t in diff_type else '0' for t in types]) )

if __name__ == '__main__':
    original_count()
    original_count_bytes()
