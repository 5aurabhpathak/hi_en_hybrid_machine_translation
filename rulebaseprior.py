#!/bin/env python3
#Author: Saurabh Pathak
#Prior rule-base
import subprocess, os
from data import run

rulechunks = None

class _RuleChunk:
    def __init__(self, begpos, length, trans):
        rulechunks.append(self)
        self.istart, self.iend, self.trans = begpos, begpos + length, trans

def apply_rules(ip, tag, l):
    '''rules to apply at the beginning'''

    global rulechunks
    rulechunks = []
    #Auxillary verbs treatment
    for i, x in enumerate(ip):
        bound, lbound = i+1 < l, i > 0
        if x in {'रहता', 'रहती', 'रहा', 'रही'} and lbound and tag[i-1]['POS'] == 'VM':
            if bound and ip[i+1] == 'हूँ': _RuleChunk(i, 2, 'have been')
            elif x in {'रहता', 'रहती'} or (x in {'रहा', 'रही'} and lbound and tag[i-1]['suffix'] in {'ता', 'ती'}):
                if bound and ip[i+1] == 'है': _RuleChunk(i, 2, 'has been')
                elif bound and ip[i+1] in {'था', 'थी'}: _RuleChunk(i, 2, 'had been')
        elif x in {'रहते', 'रहतीं', 'रहे', 'रहीं'} and lbound and tag[i-1]['POS'] == 'VM':
            if x in {'रहते', 'रहतीं'} or (x in {'रहे', 'रहीं'} and lbound and tag[i-1]['suffix'] in {'ते', 'ती'}):
                if bound and ip[i+1] == 'हैं': _RuleChunk(i, 2, 'have been')
                elif bound and ip[i+1] in {'थे', 'थीं'}: _RuleChunk(i, 2, 'had been')
        elif x == 'चाहिए':
            if bound and ip[i+1] == 'था':
                if lbound and ip[i-1] == 'होना': _RuleChunk(i, 3, 'should have been')
                else: _RuleChunk(i, 2, 'should have')
            elif lbound and tag[i-1]['POS'] == 'VM':
                if ip[i-1] == 'होना': _RuleChunk(i, 2, 'should be')
                else: _RuleChunk(i, 1, 'should')
        elif x in {'सकता', 'सकती', 'सकते','सकूँगा', 'सकूँगी', 'सकेगा', 'सकेगी', 'सकेंगे', 'सकेंगी'}:
            if x in {'सकता', 'सकती', 'सकते'}:
                if bound and ip[i+1] in {'था', 'थी', 'थे'}:
                    if lbound and ip[i-1] == 'हो': _RuleChunk(i, 3, 'could have been')
                    else: _RuleChunk(i, 2, 'could have')
                elif bound and ip[i+1] in {'हूँ', 'है', 'हैं'}: _RuleChunk(i, 2, 'can be')
                elif bound and tag[i+1]['POS'] != 'VM': _RuleChunk(i, 1, 'could')
            else: _RuleChunk(i, 1, 'can') 
        elif x in {'रहूंगा', 'रहूंगी', 'रहेंगे'}: _RuleChunk(i, 2, 'will be')
        elif x in {'होऊंगा', 'होऊंगी', 'होंगे', 'होंगी', 'होगा', 'होगी'}:
            if lbound and tag[i-1]['POS'] == 'VM':
                if ip[i-1] in {'रहा', 'रही', 'रहे', 'रही'}: _RuleChunk(i, 2, 'will have been')
                elif ip[i-1] in {'चुका', 'चुकी', 'चुके'}: _RuleChunk(i, 2, 'will have')
                elif tag[i-1]['suffix'] in {'ता', 'ते', 'ती'}: _RuleChunk(i, 1, 'will be')
            else: _RuleChunk(i, 1, 'will be')
    return rulechunks

def tag_input(inp):
    p = subprocess.Popen('./make.sh {}'.format(inp).split(), stdout=subprocess.PIPE, universal_newlines=True)
    out, err = p.communicate()
    d = []
    for line in out.splitlines():
        if 'EOL' in line: continue
        line = line.split('\t')
        d.append({x : y for x, y in zip(['POS', 'lemma', 'suffix', 'coarsePOS', 'gender', 'number', 'case'], line[1:])})
    return d

def tag_input_file(f):
    D, d = [], []
    p = subprocess.Popen('./make.sh {}'.format(f).split(), stdout=subprocess.PIPE, universal_newlines=True)
    out, err = p.communicate()
    with open('{}/tags.out'.format(run), 'w', encoding='utf-8') as tagop: tagop.write(out)
    for line in out.splitlines():
        if 'EOL' in line:
            D.append(d)
            d = []
            continue
        line = line.split('\t')
        d.append({x : y for x, y in zip(['POS', 'lemma', 'suffix', 'coarsePOS', 'gender', 'number', 'case'], line[1:])})
    return D
