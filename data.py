#!/bin/env python3
#Author: Saurabh Pathak
#Necessary data
import sys, os, subprocess

dbdir, f, e, al, run, infofile = '', '', '', '', os.environ['THESISDIR'] + '/data/run', None

class _Match: pass # <-- containers for attributes. Could use a dict instead but that means more syntax
class _Item: pass

def load():
    global dbdir, f, e, al
    print('Loading example-base...', sep='', end='', flush=True, file=sys.stderr)
    dbdir, adir = os.environ['THESISDIR'] + '/data/corpus/bilingual/parallel/lc/', os.environ['THESISDIR'] + '/data/train/lowercased/model/aligned.grow-diag-final-and'
    with open(dbdir+'IITB.en-hi.train.hi') as f, open(dbdir+'IITB.en-hi.train.en') as e, open(adir) as al: f, e, al = f.read(), e.read().splitlines(), al.read().splitlines()
    print('Done\nLoading language model. This may take 5 minutes if loading first time since boot...', sep='', end='', flush=True, file=sys.stderr)
    subprocess.Popen('cat {}/data/lm/lc/lm.en.5.probing.1.5.blm'.format(os.environ['THESISDIR']).split(), stdout=subprocess.DEVNULL).communicate()
    print('Done', flush=True, file=sys.stderr)
