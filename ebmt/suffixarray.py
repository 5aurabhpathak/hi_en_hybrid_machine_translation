#!/bin/env python3
#Author: Saurabh Pathak
#Credits: sort_bucket function is (a version) from below github link
#https://github.com/benfulton/Algorithmic-Alley/blob/master/AlgorithmicAlley/SuffixArrays/sa.py
'''Manber and Myers algorithm for suffix array creation-- creates suffixarray.data in input file directory'''
from sys import argv
from pickle import dump
from collections import defaultdict

if len(argv) != 2:
    print('A file name argument must be supplied.')
    exit(1)

def sort_bucket(bucket, order):
    d = defaultdict(list)
    for i in bucket:
        key = f[i:i+order]
        d[key].append(i)
    result = []
    for k,v in sorted(d.items()):
        if len(v) > 1: result += sort_bucket(v, order*2)
        else: result.append(v[0])
    return result

print('Reading file...', sep='', end='', flush=True)
with open(argv[1]) as f: f = tuple(f.read().split())
print('Done\nCreating data structure...', sep='', end='', flush=True)
suffixarray = sort_bucket((i for i in range(len(f))), 1)
print('Done\nWriting to disk...', sep='', end='', flush=True)
with open('/'.join(argv[1].split('/')[:-1])+'/suffixarray.data', 'wb') as f: dump(suffixarray, f)
print('Done')
