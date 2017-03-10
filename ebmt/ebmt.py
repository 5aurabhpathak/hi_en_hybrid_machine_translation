#!/bin/env python3
#Author: Saurabh Pathak
'''this module performs the first stage of the translation system
adapted from description in 2010 paper by Peter Koehn et al.'''
#from editdist import edit_dist
from pickle import load
import os

class _Match:
    '''class describing a match. Its an attribute container - attributes are also added from outside'''

    def __init__(self, seg_id, seg_len, seg_start): self.start, self.length, self.segid = seg_start, seg_len, seg_id

class EBMT:
    '''Handler class for EBMT - translation unit is a sentence.'''

    def __init__(self, dbir, alignment, metric='FMS'):
        self.__metric = metric
        with open(dbir+'suffixarray.data', 'rb') as sf, open(dbir+'ebmt.data', 'rb') as sd, open(dbir+'IITB.en-hi.train.hi') as f, open(dbir+'IITB.en-hi.train.en') as e, open(alignment) as a: self.__sf, self.__sd, self.__f, self.__e, self.__a = load(sf), load(sd), f.read().split(), e.read(), a.read()
        self.__sflen, self.__first_match = len(self.__sf), 0
        self.__last_match = self.__sflen-1

    def match(self, p):
        p = p.split()
        l = len(p)
        self.__ceilingcost = .3 * l
        M = self.__find_matches(p, l)

    def __find_matches(self, p, l):
        M = set()
        for start in range(l):
            for end in range(start + 3, l+1):
                remain = l - end
                #print('Current:', ' '.join(p[start:end]))
                N = self.__find_in_suffix_array(' '.join(p[start:end]), end-start)
                if N is None: break
                for m in N:
                    m.leftmin = abs(m.start - start)
                    if m.leftmin == 0 and start > 0: m.leftmin = 1
                    m.rightmin = abs(m.remain - remain)
                    if m.rightmin == 0 and remain > 0: m.rightmin = 1
                    mincost = m.leftmin + m.rightmin
                    if mincost > self.__ceilingcost: break
                    m.leftmax, m.rightmax = max(m.start, start), max(m.remain, remain)
                    m.pstart, m.pend = start, end
                    M.add(m)
        return M


    def __find_in_suffix_array(self, p, plen):

        def binary_search(lo, hi=self.__sflen-1, *, first=True):
            while hi >= lo:
                mid = (lo + hi) // 2
                pos = self.__sf[mid]
                k = ' '.join(self.__f[pos:pos+plen])
                #print('mid:', mid, 'k:', k)
                if k < p: lo = mid + 1
                elif k > p: hi = mid - 1
                elif first:
                    if mid == 0: return mid
                    prevpos = self.__sf[mid-1]
                    if ' '.join(self.__f[prevpos:prevpos+plen]) != k: return mid
                    hi = mid - 1
                else:
                    if mid == self.__sflen - 1: return mid
                    nextpos = self.__sf[mid+1]
                    if ' '.join(self.__f[nextpos:nextpos+plen]) != k: return mid
                    lo = mid + 1
            raise KeyError(p)

        try: self.__first_match = binary_search(self.__first_match, self.__last_match)
        except KeyError:
            self.__first_match, self.__last_match = 0, self.__sflen-1
            return
        N, self.__last_match = set(), binary_search(self.__first_match, first=False)
        for i in range(self.__first_match, self.__last_match + 1):
            m = _Match(*self.__sd[i])
            m.end = m.start + plen - 1
            m.remain = m.length - m.end
            N.add(m)
        return N

    def __FMS(self, s, i):
        '''computes the fuzzy match score'''
        self.__ed = edit_dist(s,i)
        return 1 - self.__ed[0] / max (len(s.split()), len(i.split()))

if __name__=="__main__":
    print('Loading...', sep='', end='', flush=True)
    eb = EBMT(os.environ['THESISDIR'] + '/data/corpus/bilingual/parallel/lc/', os.environ['THESISDIR'] + '/data/train/lowercased/model/aligned.grow-diag-final-and')
    print('Done')
    eb.match('दीपावली को देखते हुए मिठाई की मांग बढ़ जाती है .')
