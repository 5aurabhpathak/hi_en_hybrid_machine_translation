#!/bin/env python3
#Author: Saurabh Pathak
#Prior rule-base
import subprocess, os, data

rulechunks, j, wall = None, 0, None

class _RuleChunk:
    def __init__(self, begpos, length, trans):
        global j
        rulechunks.append(self)
        self.istart, self.iend, self.trans, self.fms = begpos, begpos + length, trans, 0.5
        if data.infofile is not None: j += 1

def apply_rules(ip, tag, l):
    '''rules to apply at the beginning'''

    global rulechunks
    rulechunks, i = [], 0
    #Auxillary verbs treatment
    while i < len(ip):
        bound, lbound, x = i+1 < l, i > 0, ip[i]
        if lbound and tag[i-1]['POS'] == 'VM':
            if x in {'रहता', 'रहती'} or (x in {'रहा', 'रही'} and lbound and tag[i-1]['suffix'] in {'ता', 'ती'}): #Present/Past Perfect Continuous - all 3 persons
                if bound and ip[i+1] == 'हूँ': _RuleChunk(i, 2, 'have been')
                elif bound and ip[i+1] == 'है': _RuleChunk(i, 2, 'has been')
                elif bound and ip[i+1] in {'था', 'थी'}: _RuleChunk(i, 2, 'had been')
            elif x in {'रहते', 'रहतीं'} or (x in {'रहे', 'रहीं'} and lbound and tag[i-1]['suffix'] in {'ते', 'ती'}):
                if bound and ip[i+1] == 'हैं': _RuleChunk(i, 2, 'have been')
                elif bound and ip[i+1] in {'थे', 'थीं'}: _RuleChunk(i, 2, 'had been')
            elif x in {'चुका', 'चुकी', 'चुके', 'दी', 'दिया', 'दिये', 'ली', 'लिया', 'लिये', 'गया', 'गई', 'गए'}: #Present/Past Perfect - all 3 persons
                if bound and ip[i+1] in {'हूँ', 'हैं'}: _RuleChunk(i, 2, 'have')
                elif bound and ip[i+1] in {'था', 'थी', 'थे', 'थीं'}: _RuleChunk(i, 2, 'had')
                elif bound and ip[i+1] == 'है': _RuleChunk(i, 2, 'has')
            i += 1
        elif x == 'चाहिए': #Modal verb
            if bound and ip[i+1] == 'था':
                if lbound and ip[i-1] == 'होना': _RuleChunk(i-1, 3, 'should have been')
                else: _RuleChunk(i, 2, 'should have')
                i += 1
            elif lbound and tag[i-1]['coarsePOS'] == 'v':
                if ip[i-1] == 'होना': _RuleChunk(i-1, 2, 'should be')
                else: _RuleChunk(i, 1, 'should')
        elif x in {'सकता', 'सकती', 'सकते','सकूँगा', 'सकूँगी', 'सकेगा', 'सकेगी', 'सकेंगे', 'सकेंगी', 'सका', 'सके', 'सकी', 'सकीं'}: #Modal verb - All tenses
            if x in {'सकता', 'सकती', 'सकते'}:
                if bound and ip[i+1] in {'था', 'थी', 'थे', 'थीं'}:
                    if lbound and ip[i-1] == 'हो': _RuleChunk(i-1, 3, 'could have been')
                    else: _RuleChunk(i, 2, 'could have')
                    i += 1
                elif bound and ip[i+1] in {'हूँ', 'है', 'हैं'}:
                    if lbound and ip[i-1] == 'हो': _RuleChunk(i-1, 3, 'can be')
                    else: _RuleChunk(i, 2, 'can')
                    i += 1
                elif not bound or tag[i+1]['coarsePOS'] != 'v':
                    _RuleChunk(i, 1, 'could')
            elif lbound and tag[i-1]['coarsePOS'] == 'v': _RuleChunk(i, 1, 'could')
        elif x in {'रहूंगा', 'रहूंगी', 'रहेंगे'} and lbound and tag[i-1]['coarsePOS'] == 'v': _RuleChunk(i, 1, 'will be') #Future Continuous
        elif x in {'होऊंगा', 'होऊंगी', 'होंगे', 'होंगी', 'होगा', 'होगी'}:
            if lbound and tag[i-1]['coarsePOS'] == 'v':
                if ip[i-1] in {'रहा', 'रही', 'रहे', 'रही', 'रहता', 'रहती', 'रहते'} and i > 1 and tag[i-2]['POS'] == 'VM': _RuleChunk(i-1, 2, 'will have been') #Future Perfect Continuous 
                elif ip[i-1] in {'चुका', 'चुकी', 'चुके', 'दी', 'दिया', 'दिये', 'ली', 'लिया', 'लिये', 'गया', 'गई', 'गए'} and i > 1 and tag[i-2]['POS'] == 'VM': _RuleChunk(i-1, 2, 'will have') #Future Perfect
                elif tag[i-1]['suffix'] in {'ता', 'ते', 'ती'}: _RuleChunk(i, 1, 'will be') #Future Continuous
            else: _RuleChunk(i, 1, 'will be')
        i += 1
    return rulechunks

def add_walls(istart, iend, tags, l, line):#reordering around conjunctions
    global j, wall
    s = ''
    for t in range(istart, iend):
        if (tags[t]['POS'] == 'CC' or tags[t]['lemma'] == 'जो') and t not in {0, l-1} and tags[t-1]['coarsePOS'] == 'v':
            s = ' '.join([s, line[t], '<wall />'])
            wall = True
            j += 1
        else: s = ' '.join([s, line[t]])
    return s

def tag_input(inp):
    p = subprocess.Popen(['{}/make.sh'.format(os.environ['THESISDIR']), '{}'.format(inp)], stdout=subprocess.PIPE, universal_newlines=True)
    out, err = p.communicate()
    d = []
    for line in out.splitlines():
        if 'EOL' in line: continue
        line = line.split('\t')
        d.append({x : y for x, y in zip(['lemma', 'POS', 'suffix', 'coarsePOS', 'gender', 'number', 'case'], line[1:])})
    return d

def tag_input_file(f):
    D, d = [], []
    p = subprocess.Popen('{}/make.sh {}'.format(os.environ['THESISDIR'], f).split(), stdout=subprocess.PIPE, universal_newlines=True)
    out, err = p.communicate()
    with open('{}/tags.out'.format(data.run), 'w', encoding='utf-8') as tagop: tagop.write(out)
    for line in out.splitlines():
        if 'EOL' in line:
            D.append(d)
            d = []
            continue
        line = line.split('\t')
        d.append({x : y for x, y in zip(['lemma', 'POS', 'suffix', 'coarsePOS', 'gender', 'number', 'case'], line[1:])})
    return D
