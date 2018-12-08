from subprocess import *
import threading
import time
import sys
import os
import time
import socket

web = sys.argv[1]
port = sys.argv[2] if len(sys.argv) > 2 else '9222'
sem = threading.Semaphore(0)

record = True if len(sys.argv) == 3 and sys.argv[2]=="record" else False
FNULL = open('/dev/null', 'w')

def run_chrome():
    # p = Popen(['chromium-browser', '--headless', '--remote-debugging-port={}'.format(port), '--disable-gpu', '--ignore-certificate-errors', '--user-data-dir=/tmp/nonexistent$(date +%s%N)', '--disk-cache-size=1'], stdout=FNULL, stderr=STDOUT)
    p = Popen(['/Applications/Chromium.app/Contents/MacOS/Chromium', '--remote-debugging-port={}'.format(port), '--ignore-certificate-errors', '--user-data-dir=/tmp/nonexistent$(date +%s%N)', '--disk-cache-size=1'], stdout=FNULL, stderr=STDOUT)
    sem.acquire()
    call(['kill', '-9', str(p.pid)])

def connect(port):
    """
    In case the chromium isn't ready before running node run.js
    """
    s = socket.socket()
    time.sleep(0.5)
    while True:
        try:
            s.connect(('localhost', int(port)))
            break
        except Exception as e:
            time.sleep(0.5)
    s.close()



chrome = threading.Thread(target=run_chrome)
chrome.start()


connect(port)
time.sleep(0.5)
try:
    call(['node', 'run.js', web, port], timeout=60)
    time.sleep(2)
except Exception as e:
    print("Chrome.py: Wrong with recording {}: {}".format(web, str(e)) )

sem.release()
chrome.join()
