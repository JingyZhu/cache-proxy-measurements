import requests
import json
from urllib.parse import urlparse
import shutil
import PIL
from hyper.contrib import HTTP20Adapter
from hyper import HTTP20Connection
import common

url = "https://mail.google.com/mail/u/0/?ui=2&view=lsimp&imp=sw-asst&ik=19a26b4939&itp=SECTIONED"

# url = "https://facebook.com/security/hsts-pixel.gif"
f = open('headers/login/gmail.com.json', 'r').read()
j = json.loads(f)

headers = None
for k, v in j['available'].items():
    if v['url'] == url:
        headers = v['headers']

for k, v in j['unavailable'].items():
    if v['url'] == url:
        headers = v['headers']



# s = requests.Session()
# s.mount('https://' + urlparse(url).netloc, HTTP20Adapter())
# r = s.get(url)
# print(len(r.content.decode()))

headers = common.strip_colon(headers)
r = requests.get(url, headers=headers, timeout=5)

print(r.text)


# mine = common.find_length(r, True)[1]
# text = r.text
# i = 0
# for i in range(len(text)):
#     if text[i] == mine[i]:
#         print(text[i], end='')
#     else:
#         break
# print('\n\n')
# print(r.text[i], mine[i])