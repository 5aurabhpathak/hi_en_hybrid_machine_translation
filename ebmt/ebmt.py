#!/bin/env python3
#Author: Saurabh Pathak
'''this module performs the first stage of the translation system
adapted from description in 2010 paper by Peter Koehn et al.'''
#from editdist import edit_dist
import os, pickle, math, collections

class _Match: pass # <-- containers for attributes. Could use a dict instead but that means more syntax
class _Item: pass

class EBMT:
    '''Handler class for EBMT - translation unit is a sentence.'''

    def __init__(self, dbir, alignment, metric='FMS'):
        self.__metric = metric
        with open(dbir+'suffixarray.data', 'rb') as sf, open(dbir+'ebmt.data', 'rb') as sd, open(dbir+'IITB.en-hi.train.hi') as f, open(dbir+'IITB.en-hi.train.en') as e, open(alignment) as a: self.__sf, self.__sd, f, self.__e, self.__a = pickle.load(sf), pickle.load(sd), f.read(), e.read(), a.read()
        self.__sflen, self.__f, self.__fl = len(self.__sf), f.split(), f.splitlines()

    def match(self, p):
        p = p.split()
        l = len(p)
        self.__ceilingcost = math.ceil(.3 * l)
        M = self.__find_matches(p, l)
        return self.__find_segments(M, l)

    def __find_segments(self, M, l):
        A, S = [], []
        for k, v in M.items():
            a = _Item()
            a.M, a.s = v, self.__fl[k]
            a.sumlength = sum([m.length for m in v])
            a.priority = - a.sumlength
            A.append(a)

        while len(A) > 0:
            a = A.pop()
            if a.M[0].length - l > self.__ceilingcost or max(a.M[0].length, l) - a.sumlength > self.__ceilingcost: continue
            cost = self.__parse_validate(a.s, a.M)
            if cost < self.__ceilingcost: self.__ceilingcost, S = cost, []
            if cost == self.__ceilingcost: S.append(a.s)
        return S

    def __parse_validate(self, s, M):
        A = []
        for m1 in M:
            for m2 in M:
                a = self.__combinable(m1, m2)
                if a is not None: A.append(a)
        cost = min([m.leftmax + m.rightmax for m in M])
        while len(A) > 0:
            a = A.pop()
            if a.mincost > self.__ceilingcost: continue
            mm = _Match()
            mm.leftmin, mm.leftmax, mm.rightmin, mm.rightmax, mm.start, mm.end, mm.pstart, mm.pend, mm.internal = a.m1.leftmin, a.m1.leftmax, a.m2.rightmin, a.m2.rightmax, a.m1.start, a.m2.end, a.m1.pstart, a.m2.pend, a.m1.internal + a.m2.internal + a.internal
            cost = min(cost, mm.leftmax + mm.rightmax + mm.internal)
            for m in M:
                a = self.__combinable(mm, m)
                if a is not None: A.append(a)
        return cost

    def __combinable(self, m1, m2):
        if m1.end >= m2.start or m1.pend >= m2.pstart: return
        a = _Item()
        a.m1, a.m2, delete, insert = m1, m2, m2.start - m1.end - 1, m2.pstart - m1.pend - 1
        a.internal = max(insert, delete)
        a.mincost = a.priority = m1.leftmin + m2.rightmin + a.internal
        return a

    def __find_matches(self, p, l):
        M = collections.defaultdict(list)
        for start in range(l):
            self.__first_match, self.__last_match = 0, self.__sflen-1
            for end in range(start + 3, l+1):
                remain = l - end
                N = self.__find_in_suffix_array(' '.join(p[start:end]), end-start)
                if N is None: break
                for m in N:
                    m.leftmin = abs(m.start - start)
                    if m.leftmin == 0 and start > 0: m.leftmin = 1
                    m.rightmin = abs(m.remain - remain)
                    if m.rightmin == 0 and remain > 0: m.rightmin = 1
                    m.leftmax, m.rightmax = max(m.start, start), max(m.remain, remain)
                    mincost, maxcost = m.leftmin + m.rightmin, m.leftmax + m.rightmax
                    self.__ceilingcost = min(maxcost, self.__ceilingcost) # <-- described in paper text but not in their pseudocode
                    if mincost > self.__ceilingcost: continue
                    m.internal, m.pstart, m.pend, k = 0, start, end, [mm for mm in M[m.segid] if not (mm.start >= m.start and mm.end <= m.end)]
                    k.append(m)
                    M[m.segid] = k
        return M


    def __find_in_suffix_array(self, p, plen):

        def binary_search(lo, hi=self.__sflen-1, *, first=True):
            while hi >= lo:
                mid = (lo + hi) // 2
                pos = self.__sf[mid]
                k = ' '.join(self.__f[pos:pos+plen])
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
            raise KeyError

        try: self.__first_match = binary_search(self.__first_match, self.__last_match)
        except KeyError: return
        N, self.__last_match = [], binary_search(self.__first_match, first=False)
        for i in range(self.__first_match, self.__last_match + 1):
            m = _Match()
            m.segid, m.length, m.start = self.__sd[self.__sf[i]]
            m.end = m.start + plen - 1
            m.remain = m.length - m.end
            N.append(m)
        return N

    def __FMS(self, s, i):
        '''computes the fuzzy match score'''
        self.__ed = edit_dist(s,i)
        return 1 - self.__ed[0] / max (len(s.split()), len(i.split()))

if __name__=="__main__":
    print('Loading...', sep='', end='', flush=True)
    eb = EBMT(os.environ['THESISDIR'] + '/data/corpus/bilingual/parallel/lc/', os.environ['THESISDIR'] + '/data/train/lowercased/model/aligned.grow-diag-final-and')
    print('Done')
    import timeit, gc
    print(timeit.Timer("eb.match('उन्होंने इस मामले की जाच करते हुए 13वें वित आयोग की राशि पर तत्काल रोक लगाने की मांग की है .')", 'gc.enable()', globals=globals()).timeit(1))
