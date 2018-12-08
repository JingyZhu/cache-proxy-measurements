"""
Get random website from top million websites
CUT is top n websites sample
"""
import re
import random
import requests

CUT=1000
SAMPLE=100
web_dict = {}
webs = open('weblist_all', 'r').readlines()
if CUT != 0:
    webs = webs[:CUT]
random.shuffle(webs)


i = 0

for web in webs:
    web = web.strip()
    web = web.split(',')
    sre = re.search('google.', web[1])
    if sre is not None and sre.start() == 0:
        continue
    web_dict[web[1]] = (web[2]=='True')
    i += 1
    if i >=SAMPLE:
        break

weblist = open('weblist', 'w+')
for web in web_dict:
    weblist.write('{},{}\n'.format(web, web_dict[web]))
weblist.close()
