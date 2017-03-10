#!/bin/env python3
#Author: Saurabh Pathak
'''Auxiliary data for ebmt --creates ebmt.data in input file directory'''
from sys import argv
from pickle import dump

if len(argv) != 2:
    print('A file name argument must be supplied.')
    exit(1)

print('Creating data structure...', sep='', end='', flush=True)
with open(argv[1]) as f: f = f.read().splitlines()
j, data = 0, {}
for i in range(len(f)):
    l = len(f[i].split())
    for x in range(j,j+l): data[x] = i, l, x-j
    j += l

print('Done\nWriting to disk...', sep='', end='', flush=True)
with open('/'.join(argv[1].split('/')[:-1])+'/ebmt.data', 'wb') as f: dump(data, f)
print('Done')
