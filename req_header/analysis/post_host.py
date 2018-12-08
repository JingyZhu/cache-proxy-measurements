import json
from urllib.parse import urlparse

f = open('post_req.json', 'r', encoding='utf-8').read()
post_json = json.loads(f)
post_list = {}

for req in post_json:
    host = urlparse(req['url']).netloc
    if host not in post_list:
        post_list[host] = 0
    post_list[host] += 1

post_list = [(k, v) for k, v in post_list.items()]
post_list.sort(key=lambda x: x[1], reverse=True)
for item in post_list:
    print(item[0] + ': ' + str(item[1]))
