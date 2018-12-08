from subprocess import *
import threading
import time
import sys
from queue import Queue
import os
import time

web = sys.argv[1]

sem = threading.Semaphore(0)

FNULL = open('/dev/null', 'w')

def run_chrome():
    Popen(['chromium-browser', '--headless', '--remote-debugging-port=9222', '--disable-gpu', '--ignore-certificate-errors', '--user-data-dir=/tmp/nonexistent$(date +%s%N)', '--disk-cache-size=1'], stdout=FNULL, stderr=STDOUT)
    sem.acquire()
    call(['pkill', 'chromium'])



chrome = threading.Thread(target=run_chrome)
chrome.start()

time.sleep(2)
call(['node', 'run.js', web])

sem.release()
