import os

def read_cookie_string(filename):
    cookie = open(filename, 'r').read()
    cookie = cookie.split(';')
    cookie_dict = {}
    for kv in cookie:
        kv = kv.split('=')
        k, v = kv[0], '='.join(kv[1:])
        cookie_dict[k.strip()] = v.strip()
    return cookie_dict

def diff_dict_keys(dict1, dict2):
    return {k: dict2[k] for k in set(dict2) - set(dict1)}

def diff_dict(dict1, dict2):
    diff = {'additional_keys': {1: [], 2: []}, 'diff_values': []}
    for k, v in dict1.items():
        if k not in dict2:
            diff['additional_keys'][1].append(k)
        elif v != dict2[k]:
            diff['diff_values'].append(k)
    for k, v in dict1.items():
        if k not in dict1:
            diff['additional_keys'][2].append(k)
    return diff

def same_dict(dict1, dict2):
    same = {}
    for k, v in dict1.items():
        if k in dict2 and v == dict2[k]:
            same[k] = v
    return same

dict1 = read_cookie_string('linkedin_mac')
dict2 = read_cookie_string('linkedin_win')

print(same_dict(dict1, dict2))
print(dict1)
print(dict2)