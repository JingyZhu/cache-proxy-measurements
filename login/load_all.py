"""
Load all webs in the scripts
If argument presented, go the taht web
Else go to all webs in weblist
"""
import os
import sys
import time
import threading
from subprocess import *

FNULL = open('/dev/null', 'w')
sem = threading.Semaphore(0)
PWD = os.environ['PWD']

weblist = [sys.argv[1]] if len(sys.argv) > 1 else open('weblist', 'r').read().split('\n')
while weblist[-1] =='':
    del weblist[-1]

def run_chrome(usr_dir):
    p = Popen(['/Applications/Chromium.app/Contents/MacOS/Chromium', '--remote-debugging-port={}'.format(9222), \
                 '--user-data-dir={}'.format(usr_dir), '--disk-cache-size=1', '--disable-site-isolation-trials'], stdout=FNULL, stderr=STDOUT)
    sem.acquire()
    call(['kill', '-9', str(p.pid)])



def login(weblist):
    chrome = threading.Thread(target=run_chrome, args=[os.path.join(PWD, 'login')])
    chrome.start()

    time.sleep(1)
    for web in weblist:
        print(web)
        try:
            call(['./login.py', web, 'new'], timeout=120)
            time.sleep(1)
        except Exception as e:
            print("Chrome.py: Wrong with recording {}: {}".format(web, str(e)) )

    sem.release()
    chrome.join()

def unlogin(weblist):
    print("Unlogin stage")
    # chrome2 = threading.Thread(target=run_chrome, args=[os.path.join(PWD, 'unlogin')])
    # chrome2.start()

    time.sleep(1)
    for web in weblist:
        print(web)
        try:
            call(['python3', 'unlogin.py', web], timeout=45)
            time.sleep(1)
        except Exception as e:
            print("load.py: Wrong with recording {}: {}".format(web, str(e)) )

# sem.release()
# chrome2.join()

if __name__ == '__main__':
    weblist = open('weblist', 'r').read().split('\n')
    while weblist[-1] =='':
        del weblist[-1]
    is_login = 'login' in sys.argv
    is_unlogin = 'unlogin' in sys.argv
    all_web = (len(sys.argv) < 2) or (bool((is_login + is_unlogin) % 2) and len(sys.argv) == 2)
    if not all_web:
        weblist = [sys.argv[1]]
    # print(all_web, is_login, is_unlogin)
    if is_login or not is_unlogin:
        login(weblist)
    if is_unlogin or not is_login:
        unlogin(weblist)
