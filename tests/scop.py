# coding: utf-8

from itertools import groupby

lst = [4, 2, 1, 5, 6, 7, 8, 11, 12, 13, 19]
for i in range(len(lst)):
    j = i+1
    for j in range(len(lst)):
        if lst[i] < lst[j]:
            x = lst[i]
            lst[i] = lst[j]
            lst[j] = x
fun = lambda x: x[0]-x[1]
for k, g in groupby(enumerate(lst), fun):
    l1 = [j for i, j in g]
    if len(l1) > 1:
        s = str(min(l1)) + '-' + str(max(l1))
    else:
        s = l1[0]
    print(s)
