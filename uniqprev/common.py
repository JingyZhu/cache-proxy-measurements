def gen_row(percent, value, thisis, total):
    begin = ['null'] * total
    begin[thisis] = str(percent)
    return '[{}, {}],\n'.format(value, ','.join(begin))

def gen_cdf(data, filename):
    """
    Data: a list of list. where 0-dim for a class, 1-dim for actual data
    """
    number_class = len(data)
    rstr = ''
    for j in range(number_class):
        i, size = 1, len(data[j])
        data[j].sort()
        for datus in data[j]:
            rstr += gen_row(i / size, datus, j, number_class)
            i += 1
        rstr += '\n\n'
    f = open(filename, 'w+')
    f.write(rstr)
    f.close()