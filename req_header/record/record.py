"""
Record all the resources into cacheable and uncacheable json
Websites list is named weblist
"""
from subprocess import *
import os
import sys
import gc
import multiprocessing

http = 'http://'
https = 'https://'

num_workers = 16
port_Queue = multiprocessing.Queue()
for i in range(9222, 9222 + num_workers):
    port_Queue.put(i)
FNULL = open(os.devnull, 'w')

web_list = open('weblist', 'r').read().split('\n')
while web_list[-1] == "":
    del web_list[-1]

def run_chrome(web, i):
    port = port_Queue.get()
    web = web.split(',')
    sys.stdout.flush()
    url = https + web[0] if web[1] == 'True' else http + web[0]
    web = web[0]
    print('{}. {} **'.format(i, web))
    try:
        call(['python3', 'chrome.py', url, str(port)], env=os.environ.copy())
    except Exception as e:
        print("Record: Wrong with recording {}: {}".format(web, str(e)) )
        gc.collect()
    port_Queue.put(port)
    sys.stdout.flush()

if __name__ == '__main__':
    p = multiprocessing.Pool(num_workers)
    total = len(web_list)
    p.starmap(run_chrome, zip(web_list, list(range(1, total + 1))))