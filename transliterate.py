#!/bin/env python3
#Author: Saurabh Pathak
#Transliteration module
from subprocess import Popen, DEVNULL
import os, data, collections

j = 0

def isHindi(word): return all(2304 <= ord(c) <= 2431 for c in word)

def translit_file(smt):
    if data.infofile is not None: global j
    d = collections.defaultdict(list)
    with open(smt) as oov, open('{}/translit.in'.format(data.run), 'w', encoding='utf-8') as inp:
        for i, line in enumerate(oov):
            words = line.split()
            for word in words:
                if isHindi(word):
                    d[i].append(word)
                    if data.infofile is not None: j += 1
                    inp.write(' '.join(list(word))+'\n')

    with open('{}/translit.out'.format(data.run), 'w', encoding='utf-8') as out:
        Popen('moses -f {}/data/train/lowercased/model/hpb/transliterate/tuning/moses.tuned.ini -i {}/translit.in'.format(os.environ['THESISDIR'], data.run).split(), stdout=out, universal_newlines=True, stderr=DEVNULL).wait()

    with open('{}/transliterated.out'.format(data.run), 'w') as enout, open('{}/translit.out'.format(data.run)) as out, open(smt) as smtout:
        key, j = list(d.keys()), 0
        key.sort()
        keylen = len(key)
        for i, line in enumerate(smtout):
            if j < keylen and i == key[j]:
                for word, t in zip(d[key[j]], out): line = line.replace(word, ''.join(t.split()), 1)
                j += 1
            enout.write(line)

def translit_sent(outstr):
    d = []
    with open('{}/translit.in'.format(data.run), 'w', encoding='utf-8') as inp:
        words = outstr.split()
        for word in words:
            if isHindi(word):
                d.append(word)
                inp.write(' '.join(list(word))+'\n')

    with open('{}/translit.out'.format(data.run), 'w', encoding='utf-8') as out:
        Popen('moses -f {}/data/train/lowercased/model/hpb/transliterate/tuning/moses.tuned.ini -i {}/translit.in'.format(os.environ['THESISDIR'], data.run).split(), stdout=out, universal_newlines=True).wait()

    with open('{}/translit.out'.format(data.run)) as out:
        for word, t in zip(d, out): outstr = outstr.replace(word, ''.join(t.split()), 1)
    return outstr
