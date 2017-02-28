#!/bin/env python3
#Author: Saurabh Pathak
'''this module performs the first stage of the translation system'''
from editdist import edit_dist
import os

class EBMT:
    '''Handler class for EBMT - translation unit is a sentence.'''

    def __init__(self, db, alignment, metric='FMS'):
        self.__metric = metric
        #read into memory all at once to avoid repititive disk access
        with open(db+'.hi') as f, open(db+'.en') as e, open(alignment) as a: self.__f, self.__e, self.__a = f.read(), e.read(), a.read()

    def match(self, sent, thresh=.5):
        '''returns matched examples'''
        i, matched_examples = 1, list()
        for hi_line in self.__f.splitlines():
            score = self.__FMS(hi_line, sent)
            if score >= thresh: matched_examples += (i, score),
            i += 1
        return matched_examples

    def __FMS(self, s, i):
        '''computes the fuzzy match score'''
        self.__ed = edit_dist(s,i)
        return 1 - self.__ed[0] / max (len(s.split()), len(i.split()))

if __name__=="__main__":
    eb = EBMT(os.environ['THESISDIR'] + '/data/corpus/bilingual/parallel/lc/IITB.en-hi.train', os.environ['THESISDIR'] + '/data/train/lowercased/model/aligned.grow-diag-final-and')
    print(eb.match('दीपावली को देखते हुए मिठाई की मांग बढ़ जाती है .'))
