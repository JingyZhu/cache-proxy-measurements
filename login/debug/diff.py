str1 = open('log', 'r').read()
str2 = open('log2', 'r').read()
strr = ''

i  = 0
while str1[i] == str2[i]:
    i += 1
    strr += str1[i]

print(i, str1[i],  str2[i] + '\n', strr)