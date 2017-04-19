#!/bin/env python3
#Author: Saurabh Pathak
'''graph visualizer for HPBSMT experiments'''
from matplotlib import pyplot as pl
from numpy import loadtxt, arange, argmax
import sys

def graph(x,y,z):
    fig = pl.figure('{} vs {}'.format(x,y), figsize=(13.66, 7.68))
    pl.plot(data[x], data[y], marker='o', markersize=5)
    pl.xlabel(x)
    pl.ylabel(y)
    if y == 'BLEU': pl.yticks(arange(min(data[y]), max(data[y])+.1, .1))
    for i, txt in enumerate(data[z]): pl.annotate(txt, (data[x][i], data[y][i]), textcoords='offset points', xytext=(10,-5))
    i = argmax(data[y])
    pl.title('Max {}: {}\nat {}: {}'.format(y, data[y][i], x, data[x][i]))
    pl.text(0, -.1, '*Annotations are in {}'.format(z), transform=pl.gca().transAxes)
    pl.savefig('{} vs {}.png'.format(x, y), format='png')
    pl.show()


if __name__=='__main__':
    p, b, r = 'Population Limit', 'BLEU', 'Runtime (m)'
    data=loadtxt(sys.argv[1], dtype=[(p,'int'), (b, 'float'), (r, 'float')])
    graph(p,b,r)
    graph(p,r,b)
