#!/anaconda3/bin/python3
"""
load the resouces with unloggedin (empty) cookie
"""
import os
import sys
import json
from subprocess import *
import requests
import common
from urllib.parse import urlparse
from hyper.contrib import HTTP20Adapter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

host = sys.argv[1]
url = 'https://' + host


def load(login):
    compare = {'same': {}, 'diff': {}}
    for _, req in login.items():
        if "bytes" not in req:
            continue
        if req['method'] == 'GET' and 'headers' in req and ('cookie' in req['headers'] or 'Cookie' in req['headers']):
            try:
                if 'cookie' in req['headers']:
                    del req['headers']['cookie']
                else:
                    del req['headers']['Cookie']
                # s = requests.Session()
                # s.mount("https://" + urlparse(req['url']).netloc, HTTP20Adapter())
                # r = s.get(req['url'], headers=req['headers'], timeout=5)
                headers = common.strip_colon(req['headers'])
                r = requests.get(req['url'], headers=headers, timeout=10)
            except Exception as e: 
                print(str(e))
                continue
            byte, text = common.find_length(r, True)
            is_similar, similarity = common.similar(byte, req['bytes'], text, check_output(['python3', 'extract_resource.py', host.replace('/', '_'), req['url']]).decode())
            if is_similar:
                compare['same'][req['url']] = [byte]
            else:
                compare['diff'][req['url']] = [byte, req['bytes'], similarity]
    f = open(os.path.join('headers', 'compare', host.replace('/', '_') + '.json'), 'w+')
    f.write(json.dumps(compare))

def identical_response(byte, body, req, resource):
    if req['type'] in ['Document', 'XHR', 'Fetch', 'Script']:
        return byte == req['bytes']
    return body == resource['body']



# def find_length(r):
#     if 'content-encoding' in r.headers and r.headers['content-encoding'] == 'br':
#         return (len(brotli.decompress(r.content)),  brotli.decompress(r.content))
#     else:
#         return (len(base64.b64encode(r.content)), base64.b64encode(r.content).decode())


f = open(os.path.join('headers', 'login', host.replace('/', '_') + '.json'), 'r').read()
login_json = json.loads(f)
load(login_json['available'])
