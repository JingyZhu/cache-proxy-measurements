"""
Run node run.js web for 3 times
keep the mean #resources one
"""
import login
import sys


if __name__ == '__main__':
    weblist = [sys.argv[1]] if len(sys.argv) > 1 else open('weblist', 'r').read().split('\n')
    while weblist[-1] =='':
        del weblist[-1]
    for web in weblist:
        login.multiple_loads(3, 'https://' + web)