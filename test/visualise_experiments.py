#!/bin/env python3
#Author: Saurabh Pathak
'''graph visualizer for experiments'''
from matplotlib import pyplot as pl
from numpy import zeros
from os import chdir

def figplot(prefix, output='../../../../'):
    with open(prefix+'.en', encoding='utf-8') as en_ip, open(prefix+'.hi', encoding='utf-8') as hi_ip:
        de, dh, f, num_lines = dict(), dict(), dict(), len(en_ip.readlines())
        en_ip.seek(0)
        for hi_line, en_line in zip(hi_ip, en_ip):
            i, j = len(en_line), len(hi_line)
            de[i] = de.get(i, 0) + 1
            dh[i] = dh.get(i, 0) + 1
            f[round(i/j)] = f.get(round(i/j), 0) + 1
    pl.figure('Sentence lengths / Fertility -- '+prefix, figsize=(19,10))
    #pl.subplot(131)
    pl.title('en')
    pl.plot(range(len(de)), list(de.values()))
    pl.xticks(range(0, len(de), 100), list(de.keys())[::100])
    pl.tight_layout(0)
    #pl.subplot(132)
    #pl.title('hi')
    #pl.plot(list(range(1, num_lines+1)), lh)
    #pl.subplot(133)
    #pl.title('fertility ratios')
    #pl.plot(list(range(1, num_lines+1)), fr)
    pl.savefig(output+prefix.split('/')[-1]+'.png', format='png')

if __name__=="__main__":
    chdir('../data/corpus/bilingual/parallel/')
    figplot('IITB.en-hi.true')
    #figplot('IITB.en-hi.clean')
    #figplot('IITB.en-hi.train')
    #figplot('filtered_out/IITB.en-hi.err')
    #figplot('selected_out/IITB.en-hi.sep')
