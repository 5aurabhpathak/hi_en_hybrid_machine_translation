#!/bin/env python3
#Author: Saurabh Pathak
#Transliteration module
from subprocess import Popen, PIPE
import os, data

def translit_file(oovfile, smt):
    d = {}
    with open(oovfile) as oov, open('{}/translit.in'.format(data.run), 'w', encoding='utf-8') as inp:
        for i, line in enumerate(oov):
            words = line.split()
            if words != []: d[i] = words
            for word in words: inp.write(' '.join(list(word)))

    with open('{}/translit.out'.format(data.run), 'w', encoding='utf-8') as out:
        Popen('moses -f {}/data/train/lowercased/model/hpb/transliterate/tuning/moses.tuned.ini -i {}/translit.in'.format(os.environ['THESISDIR'], data.run).split(), stdout=out, universal_newlines=True).wait()
        out.flush()
        with open('{}/en.out'.format(data.run), 'w', encoding='utf-8') as enout:
            for k in d.keys():
                for i, line in enumerate(smt):
                    if i == k:
                        for word, t in zip(d[k], out): line.replace(word, t, 1)
                    enout.write(line)

def translit_sent(oovfile, outstr):
    with open(oovfile) as oov, open('{}/translit.in'.format(data.run), 'w', encoding='utf-8') as inp:
        words = line.split()
        for word in words: inp.write(' '.join(list(word)))

    with open('{}/translit.out'.format(data.run), 'w', encoding='utf-8') as out:
        Popen('moses -f {}/data/train/lowercased/model/hpb/transliterate/tuning/moses.tuned.ini -i {}/translit.in'.format(os.environ['THESISDIR'], data.run).split(), stdout=out, universal_newlines=True).wait()
        out.flush()
        for word, t in zip(words, out): outstr.replace(word, t, 1)
    return outstr
