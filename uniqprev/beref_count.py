import json
import os
from os.path import join
import common

web_list = os.listdir('crawl')

url_count = {}

for web in web_list:
    obj = json.loads(open(join('crawl', web), 'r').read())
    for event in obj:
        if event['method'] == 'Network.requestWillBeSent':
            url = event['params']['request']["url"]
            if url not in url_count:
                url_count[url] = 0
            url_count[url] += 1

common.gen_cdf([list(url_count.values())], 'url_beref.log')