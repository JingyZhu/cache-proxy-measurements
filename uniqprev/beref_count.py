import json
import os
from os.path import join
import common
from urllib.parse import urlparse

web_list = os.listdir('crawl')

url_count = {'orig': {}, 'filt': {}}

for web in web_list:
    obj = json.loads(open(join('crawl', web), 'r').read())
    for event in obj:
        if event['method'] == 'Network.requestWillBeSent':
            orig_url = event['params']['request']["url"]
            parse_result = urlparse(orig_url)
            filt_url = '{}://{}'.format(parse_result.scheme, parse_result.netloc + parse_result.path)
            if orig_url not in url_count['orig']:
                url_count['orig'][orig_url] = 0
            url_count['orig'][orig_url] += 1
            if filt_url not in url_count['filt']:
                url_count['filt'][filt_url] = 0
            url_count['filt'][filt_url] += 1

common.gen_cdf([list(url_count['orig'].values()), list(url_count['filt'].values())], 'url_beref.log')