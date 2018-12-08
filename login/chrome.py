#!/anaconda3/bin/python3
from subprocess import *
import threading
import time
import sys
import os
import time
import socket
import signal

def exit_scirpt(sig, frame):
    print('')
    exit(1)

signal.signal(signal.SIGINT, exit_scirpt)

usr_dir = sys.argv[1] if len(sys.argv) > 1 else '/tmp/nonexistent{}%N)'.format(round(time.time()))
sem = threading.Semaphore(0)

FNULL = open('/dev/null', 'w')

def run_chrome():
    call(['/Applications/Chromium.app/Contents/MacOS/Chromium', '--remote-debugging-port=9222', \
            '--user-data-dir={}'.format(usr_dir), '--disk-cache-size=1', '--disable-site-isolation-trials'])

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


run_chrome()
