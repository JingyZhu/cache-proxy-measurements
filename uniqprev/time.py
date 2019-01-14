#!/anaconda3/bin/python3
import subprocess
import time
import sys

argc = len(sys.argv)

begin = time.time()
subprocess.call(sys.argv[1:])
end = time.time()
print(end - begin)