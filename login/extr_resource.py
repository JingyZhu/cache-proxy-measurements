"""
Extract certain response body
"""
import os
import json
import sys


def extr_resource(host, url):
    resource_json = json.loads(open(os.path.join('headers', 'resources', host.replace('/', '_') + '.json'), 'r').read())
    body = resource_json[url]['body']
    if type(body) is bytes:
        return body.decode()
    else:
        return body

if __name__ == '__main__':
    host = sys.argv[1]
    url = sys.argv[2]
    print(extr_resource(host, url))