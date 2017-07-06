#!/bin/env python3
#Author: Saurabh Pathak
'''graph visualizer for HPBSMT experiments'''
from matplotlib import animation as an, pyplot as pl, rcParams
from mpl_toolkits.mplot3d import Axes3D
from numpy import loadtxt, arange, argmax
import sys, getopt

def graph(x,y,z):
    fig = pl.figure('{} vs {}'.format(x,y), figsize=(13.66, 7.68))
    pl.plot(data[x], data[y], marker='o', markersize=5)
    pl.xlabel(x)
    pl.ylabel(y)
    if y == 'BLEU': pl.yticks(arange(min(data[y]), max(data[y])+.1, .1))
    for i, txt in enumerate(data[z]): pl.annotate(round(txt,1), (data[x][i], data[y][i]), textcoords='offset points', xytext=(10,-5))
    i = argmax(data[y])
    pl.title('Max {}: {}\nat {}: {}'.format(y, data[y][i], x, data[x][i]))
    pl.text(0, -.2, '*Annotations are in {}'.format(z), transform=pl.gca().transAxes)
    fig.set_size_inches(5, 5)
    pl.savefig('{} vs {}.png'.format(x, y), format='png')
    if draw: pl.show()
    else: pl.close()

def graph3D():
    '''creates animated plot in 3D'''
    fig = pl.figure('3D Plot')
    ax = pl.subplot(projection='3d')
    ax.plot(data[p], data[b], data[r], marker='o', markersize=5)
    ax.set_xlabel(p)
    ax.set_ylabel(b)
    ax.set_zlabel(r)
    ax.view_init(elev=90, azim=-90)
    anim = an.FuncAnimation(fig, lambda i: ax.view_init(elev=i, azim=-90), frames=90, interval=20, repeat_delay=700)
    anim.save('anim3dplot.gif', writer='imagemagick', fps=15)
    if draw: pl.show()
    else: pl.close()

def usage():
    print('Usage: visualise_hpbresults.py --input hpbbleu_file [--show-plots]')
    exit(1)

if __name__=='__main__':
    opts, args = getopt.getopt(sys.argv[1:], None, ['show-plots', 'input='])
    if len(args) > 0 or not 1 <= len(opts) <= 2:
        print('Invalid arguments or fewer parameters.')
        usage()
    draw = False
    for o, a in opts:
        if o == '--show-plots': draw = True
        elif o == '--input': ip = a
        else:
            print('Invalid parameters.')
            usage()
    p, b, r = 'Population Limit', 'BLEU', 'Runtime (minutes)'
    data=loadtxt(ip, dtype=[(p,'int'), (b, 'float'), (r, 'float')])
    rcParams.update({'font.size': 14})
    graph(p,b,r)
    #graph(p,r,b)
    #graph3D()
