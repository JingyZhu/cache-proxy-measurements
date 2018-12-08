"""
Clean all cacheable and uncacheable json files
"""
from subprocess import *

call('rm headers/cacheable/*', shell=True)
call('rm headers/uncacheable/*', shell=True)

call('rm counts/*', shell=True)
call('rm bytes/*', shell=True)
