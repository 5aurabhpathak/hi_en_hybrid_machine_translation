#!/bin/env python3
#Author: Saurabh Pathak
'''graph visualizer for corpus'''
from matplotlib import pyplot as pl
from statistics import mean
from os import environ

def figplot(prefix, output=environ['THESISDIR']+'/data/'):
    with open(prefix+'.en', encoding='utf-8') as en_ip, open(prefix+'.hi', encoding='utf-8') as hi_ip:
        de, dh, f, k = [], [], [], 0
        for hi_line, en_line in zip(hi_ip, en_ip):
            i, j = len(en_line.split()), len(hi_line.split())
            de += i,
            dh += j,
            if j != 0: f += i/j,
            k += 1
    pl.figure('Sentence lengths / Fertility -- '+prefix, figsize=(12,7))
    pl.suptitle('Mean fertility ratio: {}\nNumber of pairs: {}'.format(round(mean(f), 4), k))

    def plotter(t,n,a):
        pl.subplot(n)
        pl.title(t)
        pl.hist(a, bins=range(0,101,10))
        pl.xlim(xmin=0)
        pl.ylim(ymin=0)

    plotter('en', 121, de)
    plotter('hi', 122, dh)
    pl.savefig(output+prefix.split('/')[-1]+'.png', format='png')
    pl.show()

if __name__=="__main__":
    figplot(environ['THESISDIR']+'/data/corpus/bilingual/parallel/IITB.en-hi.train')
