"""
Analyze the fraction of cacheable and uncacheble based on resource type
Count the fraction of each type of resource's request by counts and bytes over a websites
Counr the max-age of each type of resource's request
"""
import os
import json
import re

cacheable_list = os.listdir('headers/cacheable')
uncacheable_list = os.listdir('headers/uncacheable')
resource_type = {"Document", "Font", "Image", "Stylesheet", "Script", "XHR"}

def gen_row(percent, value, thisis, total):
    begin = ['null'] * total
    begin[thisis] = str(percent)
    return '[{}, {}],\n'.format(value, ','.join(begin))

def total_count():
    resource_type = {} # {'type': [cacheable, uncacheable, cachebytes. uncachebytes]}
    total_sum = 0
    cacheable_count = 0
    uncacheable_count = 0
    cacheable_bytes = 0
    uncacheable_bytes = 0
    total_bytes = 0

    for cache_file in cacheable_list:
        cache_file = os.path.join('headers', 'cacheable', cache_file)
        file = open(cache_file, 'r', encoding='utf-8').read()
        cache_json = json.loads(file)
        for req in cache_json.values():
            rtype = req['type']
            if rtype not in resource_type:
                resource_type[rtype] = [0, 0, 0, 0]
            resource_type[rtype][0] += 1
            byte = req['bytes'] if 'bytes' in req else 1
            resource_type[rtype][2] += byte

    for uncache_file in uncacheable_list:
        uncache_file = os.path.join('headers', 'uncacheable', uncache_file)
        file = open(uncache_file, 'r', encoding='utf-8').read()
        uncache_json = json.loads(file)
        for req in uncache_json.values():
            rtype = req['type']
            if rtype not in resource_type:
                resource_type[rtype] = [0, 0, 0, 0]
            resource_type[rtype][1] += 1
            byte = req['bytes'] if 'bytes' in req else 1
            resource_type[rtype][3] += byte

    for count in resource_type.values():
        cacheable_count += count[0]
        uncacheable_count += count[1]
        total_sum += count[0] + count[1]
        cacheable_bytes += count[2]
        uncacheable_bytes += count[3]
        total_bytes += count[2] + count[3]

    print('Resource\tcacheable\tuncacheable\tfraction')
    for rtype, count in resource_type.items():
        together = count[0] + count[1]
        print('{}\t{}\t{}\t{}'.format(rtype, '%.3f' % (count[0]/together), '%.3f' % (count[1]/together), '%.3f' % (together/total_sum) ))
    print('Total\t', '%.3f' % (cacheable_count/total_sum), '\t', '%.3f' % (uncacheable_count/total_sum), '\t1.0')

    print('\n\n')
    for rtype, count in resource_type.items():
        together = count[2] + count[3]
        print('{}\t{}\t{}\t{}'.format(rtype, '%.3f' % (count[2]/together), '%.3f' % (count[3]/together), '%.3f' % (together/total_bytes) ))
    print('Total\t', '%.3f' % (cacheable_bytes/total_bytes), '\t', '%.3f' % (uncacheable_bytes/total_bytes), '\t1.0')



def type_count_per_website():
    """
    Count the resource fraction for each of the website 
    """
    counts = {res_type: [] for res_type in resource_type}
    byte = {res_type: [] for res_type in resource_type}
    for webfile in cacheable_list:
        cache_file = os.path.join('headers', 'cacheable', webfile)
        file = open(cache_file, 'r').read()
        cache_json = json.loads(file)
        uncache_file = os.path.join('headers', 'uncacheable', webfile)
        file = open(uncache_file, 'r').read()
        uncache_json = json.loads(file)
        total_counts = total_bytes = 0
        want_counts =  {res_type: 0 for res_type in resource_type}
        want_bytes = {res_type: 0 for res_type in resource_type}
        for req in cache_json.values():
            length = req['bytes'] if 'bytes' in req else 0
            total_counts += 1
            total_bytes += length
            if req['type'] in resource_type:
                want_counts[req["type"]] += 1
                want_bytes[req["type"]] += length
        for req in uncache_json.values():
            length = req['bytes'] if 'bytes' in req else 0
            total_counts += 1
            total_bytes += length
            if req['type'] in resource_type:
                want_counts[req['type']] += 1
                want_bytes[req['type']] += length
        for typ in resource_type:
            if total_counts == 0:
                counts[typ].append(0)
                byte[typ].append(0)
            else:
                counts[typ].append( want_counts[typ] / total_counts)
                byte[typ].append( want_bytes[typ] / total_bytes)
            # print(want_counts[typ] / total_counts, want_bytes[typ] / total_bytes)

    resource_str = "data.addColumn('number', 'X');\n"
    byte_str = "data.addRows([\n\n"
    count_str = "data.addRows([\n\n"
    thisis = 0
    for typ in resource_type:
        resource_str += "data.addColumn('number', '{}');\n".format(typ)
        counts[typ].sort()
        byte[typ].sort()
        size = len(counts[typ])
        assert(len(counts[typ]) == len(byte[typ]))
        for i in range(size):
            count_str += gen_row( (i+1) / size, counts[typ][i], thisis, len(resource_type))
            byte_str += gen_row( (i+1) / size, byte[typ][i], thisis, len(resource_type))
            # print(counts[typ][i], byte[typ][i])
        thisis += 1
    
    byte_str += "\n\n]);"
    count_str += "\n\n]);"

    filename =  'total'
    count_file = open(os.path.join('counts', filename), 'w+')
    byte_file = open(os.path.join('bytes', filename), 'w+')

    count_file.write(resource_str)
    count_file.write(count_str)

    byte_file.write(resource_str)
    byte_file.write(byte_str)

def max_age():
    type_age = {typ: [] for typ in resource_type}
    for webfile in cacheable_list:
        cache_file = os.path.join('headers', 'cacheable', webfile)
        file = open(cache_file, 'r').read()
        cache_json = json.loads(file)
        for req in cache_json.values():
            if req['type'] in resource_type:
                response = {k.lower():v for k, v in req['response'].items()}
                try:
                    age = float(re.findall(r'\d+', response['cache-control'])[0])
                except Exception as e:
                    print(e)
                    continue
                type_age[req['type']].append(age)
    
    resource_str = "data.addColumn('number', 'X');\n"
    maxage = "data.addRows([\n\n"

    thisis = 0
    for typ in resource_type:
        resource_str += "data.addColumn('number', '{}');\n".format(typ)
        type_age[typ].sort()
        size = len(type_age[typ])
        for i in range(size):
            maxage += gen_row( (i+1)/size, type_age[typ][i], thisis, len(resource_type))
        thisis += 1

    maxage += "\n\n]);"
    maxage_file = open('maxage.log', 'w+')
    maxage_file.write(resource_str)
    maxage_file.write(maxage) 
    maxage_file.close()

# max_age()
total_count()
# type_count_per_website()
