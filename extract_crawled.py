import subprocess
import os
import json
from os.path import join
import shutil

web_list = os.listdir('0')
for web in web_list:
    network_dir = os.listdir(join('0', web))
    network_file = list(filter(lambda x: 'network_' in x, network_dir))
    newname = network_file[0][network_file[0].find('network_') + len('network_'):]
    shutil.copy(join('0', web, network_file[0]), join('uniqprev', 'crawl', newname))
