#!/bin/env python3
#Author: Saurabh Pathak
#Necessary data
import sys, os

dbdir, f, e, al = '', '', '', ''

class _Match: pass # <-- containers for attributes. Could use a dict instead but that means more syntax
class _Item: pass

def load():
    global dbdir, f, e, al
    dbdir, adir = os.environ['THESISDIR'] + '/data/corpus/bilingual/parallel/lc/', os.environ['THESISDIR'] + '/data/train/lowercased/model/aligned.grow-diag-final-and'
    with open(dbdir+'IITB.en-hi.train.hi') as f, open(dbdir+'IITB.en-hi.train.en') as e, open(adir) as al: f, e, al = f.read(), e.read().splitlines(), al.read().splitlines()
