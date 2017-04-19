#!/bin/env python3
#Author: Saurabh Pathak
'''this module performs the first stage of the translation system
partially adapted from description in 2010 paper by Peter Koehn et al.'''
from editdist import edit_dist
import os, pickle, math, collections, bisect

class _Match: pass # <-- containers for attributes. Could use a dict instead but that means more syntax
class _Item: pass

class _BestMatch:
    '''Handler class for EBMT - translation unit is a sentence.'''

    def __init__(self, dbdir, *, thresh=.3):
        self.__threshold = thresh
        with open(dbdir+'suffixarray.data', 'rb') as sf, open(dbdir+'ebmt.data', 'rb') as sd: self.__sf, self.__sd = pickle.load(sf), pickle.load(sd)
        self.__sflen, self.__f, self.__fl = len(self.__sf), f.split(), f.splitlines()

    def match(self):
        d1, d2 = collections.defaultdict(list), collections.defaultdict(list)
        for i in range(l):
            d1[line[i]].append(i)
            if i < l-1: d2[' '.join(line[i:i+2])].append(i)
        self.__ceilingcost = math.ceil(self.__threshold * l)
        #print('ceil before:', self.__ceilingcost)
        M = self.__find_matches()
        #print('ceil after', self.__ceilingcost)
        S = self.__find_segments(M, d1, d2)
        return self.__best_match(S) if len(S) > 1 else S[0]

    def __find_segments(self, M, d1, d2):
        A, S = [], []
        for k, v in M.items():
            if len(v) == 0: continue
            a = _Item()
            a.M, a.s = v, self.__fl[k]
            a.sumlength = sum([m.length for m in v])
            a.priority = - a.sumlength
            A.append(a)

        while len(A) > 0:
            a = A.pop()
            if a.M[0].length - l > self.__ceilingcost or max(a.M[0].length, l) - a.sumlength > self.__ceilingcost: continue
            #print('sentence under question', a.M[0].segid, a.s)
            t = a.s.split()
            u = len(t)
            #print('before', len(a.M))
            #for m in a.M: print(' '.join(a.s.split()[m.start:m.end]))
            for i in range(u):
                bigram = ' '.join(t[i:i+2]) if i < u-1 else None
                for start in d2.get(bigram, []):
                    end, m = start+2, _Match()
                    m.segid, m.length, m.start, m.end = a.M[0].segid, u, i, i+2
                    m.remain = m.length - m.end
                    a.M = self.__add_match(m, a.M, start, end, l-end)
                else:
                    for start in d1.get(t[i], []):
                        end, m = start+1, _Match()
                        m.segid, m.length, m.start, m.end = a.M[0].segid, u, i, i+1
                        m.remain = m.length - m.end
                        a.M = self.__add_match(m, a.M, start, end, l-end)
            #print('after', len(a.M))
            a.M.sort(key=lambda x: x.start)
            #for m in a.M: print(' '.join(a.s.split()[m.start:m.end]))
            cost = self.__parse_validate(a.M)
            #print(cost, self.__ceilingcost)
            if cost < self.__ceilingcost: self.__ceilingcost, S = cost, [a]
            elif cost == self.__ceilingcost: S.append(a)
        return S

    def __parse_validate(self, M):
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
        a.m1, a.m2, a.internal = m1, m2, max(m2.start - m1.end - 1, m2.pstart - m1.pend - 1)
        a.mincost = a.priority = m1.leftmin + m2.rightmin + a.internal
        return a

    def __find_matches(self):
        M = collections.defaultdict(list)
        for start in range(l):
            self.__first_match, self.__last_match = 0, self.__sflen-1
            for end in range(start + 3, l+1):
                N = self.__find_in_suffix_array(' '.join(line[start:end]), end-start)
                if N is None: break
                for m in N: M[m.segid] = self.__add_match(m, M[m.segid], start, end, l-end)
        return M

    def __add_match(self, m, M, start, end, remain):
        k = []
        for mm in M:
            if (mm.end >= m.end and mm.start <= m.start) or (mm.pend >= end and mm.pstart <= start): return M
            elif m.start <= mm.start <= m.end and m.start <= mm.end <= m.end: continue
            k.append(mm)
        m.leftmin = abs(m.start - start)
        if m.leftmin == 0 and start > 0: m.leftmin = 1
        m.rightmin = abs(m.remain - remain)
        if m.rightmin == 0 and remain > 0: m.rightmin = 1
        m.leftmax, m.rightmax, mincost = max(m.start, start), max(m.remain, remain), m.leftmin + m.rightmin
        #I found that both the following lines have a negative impact (incorrect output in many cases). See my thesis
        #self.__ceilingcost = min(m.leftmax + m.rightmax, self.__ceilingcost)  # <-- also, this line is described in paper text but not in their pseudocode
        #if mincost > self.__ceilingcost: return M
        m.internal, m.pstart, m.pend = 0, start, end
        k.append(m)
        return k

    def __find_in_suffix_array(self, p, plen):

        def binary_search(lo, hi=self.__sflen-1, *, first=True):
            '''to find first/last (as requested in parameter) occurence of string in text'''
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
            m.end = m.start + plen
            m.remain = m.length - m.end
            N.append(m)
        return N

    def __best_match(self, S):
        score, best = 1 / len(S[0].M), S[0]
        for a in S[1:]:
            fms = 1 / len(a.M)
            if fms > score: score, best = fms, a
            elif fms == score: best = a if edit_dist(a.s,line) < edit_dist(best.s,line) else best
        return best

def align(item):

    def mismatch(sstart, sentend):
        nonlocal matched_target
        for i in range(sstart, sentend):
            for t in alignment.get(i, []): matched_target[t] = False

    def merge_chunks():
        nonlocal chunks, lenchunks
        i = 0
        while i < lenchunks-1:
            if (chunks[i+1].pstart == chunks[i].pend or chunks[i+1].pstart == chunks[i].pstart) and (chunks[i+1].start == chunks[i].end or chunks[i+1].start == chunks[i].start):
                chunks[i].pend, chunks[i].iend, chunks[i].end = chunks[i+1].pend, chunks[i+1].iend, chunks[i+1].end
                chunks.remove(chunks[i+1])
                lenchunks -= 1
            else: i += 1

    def grow_chunk(i, j):
        nonlocal chunks, matched_target
        if j is not None: matched_target[j] = False
        for k in range(lenchunks):
            sside = 'chunks[k].pstart -= 1; chunks[k].istart -= 1' if i == chunks[k].pstart-1 else 'chunks[k].pend += 1; chunks[k].iend += 1' if i == chunks[k].pend else None
            if sside is None: continue
            if j is None:
                exec(sside)
                return True
            tside = 'chunks[k].start -= 1' if j == chunks[k].start-1 else 'chunks[k].end += 1' if i == chunks[k].end else None
            if tside is None: continue
            exec('{};{}'.format(sside, tside))
            return True
        return False

    #print(item.s)
    #for m in item.M: print(' '.join(item.s.split()[m.start:m.end]), m.pstart, m.pend, m.start, m.end)
    segid, alignment = item.M[0].segid, collections.defaultdict(list)
    for x, y in map(lambda p: tuple(map(int, p.split('-'))), a[segid].split()): alignment[x].append(y)
    target, item.s = e[segid].split(), item.s.split()
    istart = sstart = 0
    slen, tlen, d = len(item.s), len(target), None
    matched_target = [True] * tlen
    #print(alignment)
    for i in range(len(item.M)):
        m = item.M[i]
        if m.pstart < istart:
            d = i
            continue
        mismatch(sstart, m.start)
        istart, sstart = m.pend, m.end
    if sstart < slen: mismatch(sstart, slen)
    if d is not None: del item.M[d]
    #print(matched_target)
    chunks, lenchunks = [], 0
    for m in item.M:
        for i, k in zip(range(m.start, m.end), range(m.pstart, m.pend)):
            al = alignment.get(i)
            if al is not None:
                for j in al:
                    if matched_target[j] and not grow_chunk(i, j):
                        chunk = _Match()
                        chunk.pstart, chunk.pend, chunk.start, chunk.end, chunk.istart, chunk.iend = i, i+1, j, j+1, k, k+1
                        chunks.append(chunk)
                        lenchunks += 1
            else: grow_chunk(i, None)
    merge_chunks()
    #for m in chunks: print(' '.join(target[m.start:m.end]), ' '.join(item.s[m.pstart:m.pend]), m.istart, m.iend, m.pstart, m.pend, m.start, m.end)
    return chunks, target

def construct_xml(chunks, target):
    i, xml = 0, ''
    for m in chunks:
        xml += '{} <xml translation={} > {} </xml> '.format(' '.join(line[i:m.istart]), ' '.join(target[m.start:m.end]), ' '.join(line[m.istart:m.iend]))
        i = m.iend
    return xml + ' '.join(line[i:l])

if __name__=="__main__":
    dbdir, adir = os.environ['THESISDIR'] + '/data/corpus/bilingual/parallel/lc/', os.environ['THESISDIR'] + '/data/train/lowercased/model/aligned.grow-diag-final-and'
    print('Loading...', sep='', end='', flush=True)
    with open(dbdir+'IITB.en-hi.train.hi') as f, open(dbdir+'IITB.en-hi.train.en') as e, open(adir) as a: f, e, a = f.read(), e.read().splitlines(), a.read().splitlines()
    bm = _BestMatch(dbdir)
    print('Done')
    with open('{}/testsents.txt'.format(os.environ['HOME'])) as ip:
        i = 1
        for line in ip:
            line = line.split()
            l = len(line)
            print(construct_xml(*align(bm.match())))
            i += 1
