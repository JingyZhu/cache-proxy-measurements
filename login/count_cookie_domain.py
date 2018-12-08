"""
Count fractions of requests with cookie headers by domain.
"""
import os
import json
import sys
from urllib.parse import urlparse

host = sys.argv[1]
filename = os.path.join('headers', 'login', host.replace('/', '_') + '.json')
login_json = json.loads(open(filename, 'r').read())

domain_cookies = {}
urls = {}

for _, v in login_json['available'].items():
    if v['url'] in urls:
        continue
    else:
        urls[v['url']] = 1
    host = urlparse(v['url']).netloc
    if host not in domain_cookies:
        domain_cookies[host] = [0, 0]
    domain_cookies[host][1] += 1
    if 'headers' in v and ('cookie' in v['headers'] or 'Cookie' in v['headers']):
        domain_cookies[host][0] += 1

for _, v in login_json['unavailable'].items():
    if v['url'] in urls:
        continue
    else:
        urls[v['url']] = 1
    host = urlparse(v['url']).netloc
    if host not in domain_cookies:
        domain_cookies[host] = [0, 0]
    domain_cookies[host][1] += 1
    if 'headers' in v and ('cookie' in v['headers'] or 'Cookie' in v['headers']):
        domain_cookies[host][0] += 1 

print(domain_cookies)