#!/anaconda3/bin/python3
from subprocess import call

call('rm headers/compare/*', shell=True)
call('rm headers/login/*', shell=True)
call('rm headers/resources/*', shell=True)