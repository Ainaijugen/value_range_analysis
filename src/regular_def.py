import re
import random

re_float = re.compile(r'^[-+]?([0-9]+(\.[0-9]+)?|\.[0-9]+)([eE][-+]?[0-9]+)?$')
re_int = re.compile(r'^[-+]?[0-9]+$')
re_def = re.compile(r'^([a-zA-Z@0-9]*)_[0-9]+$')
re_op = re.compile(r'^[+\-*/=]$')
string = 'i@1_3'

result = re_float.search(string)
print(result)

string = 'if (k_1 <= 99) goto <bb 3>; else goto <bb 8>;'
string = string.split()
for i in range(len(string)):
    print(i, string[i])

inf = float('inf')
inf2 = float('inf')
if inf == float('inf'):
    print('yes')
else:
    print('no')


def intersection(a, b):
    ans = [1] * 4
    if a[2] < b[2]:  # a[2] b[2]
        ans[0] = b[0]
        ans[2] = b[2]
        if a[3] < b[2] or (a[3] == b[2] and a[1] & b[0] == 0):
            return None
        if b[3] < a[3]:
            ans[1] = b[1]
            ans[3] = b[3]
        elif a[3] < b[3]:
            ans[1] = a[1]
            ans[3] = a[3]
        else:
            ans[1] = a[1] & b[1]
            ans[3] = a[3]
    elif a[2] > b[2]:  # b[2] a[2]
        ans[0] = a[0]
        ans[2] = a[2]
        if b[3] < a[2] or (b[3] == a[2] and b[1] & a[0] == 0):
            return None
        if a[3] < b[3]:
            ans[1] = a[1]
            ans[3] = a[3]
        elif b[3] < a[3]:
            ans[1] = b[1]
            ans[3] = b[3]
        else:
            ans[1] = a[1] & b[1]
            ans[3] = a[3]
    else:
        ans[0] = a[0] & b[0]
        ans[2] = a[2]
        if a[3] < b[3]:
            ans[3] = a[3]
            ans[1] = a[1]
        elif a[3] > b[3]:
            ans[3] = b[3]
            ans[1] = b[1]
        else:
            ans[3] = a[3]
            ans[1] = a[1] & b[1]
    return tuple(ans)

a = 2.5
b = -2.5
a = int(a)
b = int(b)
print(a,b)
