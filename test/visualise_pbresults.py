#!/bin/env python3
#Author: Saurabh Pathak
'''graph visualizer for PBSMT experiment results'''
from matplotlib import animation as an, pyplot as pl, rcParams
from mpl_toolkits.mplot3d import Axes3D
from numpy import loadtxt, arange, argmax, array
import sys, getopt

def graph_col1vscol2(x, y, z):
    fig = pl.figure('{} vs {}'.format(x,y), figsize=(13.66, 7.68))
    i = 1
    while data[z][i] == data[z][0]: i += 1
    j = k = 0
    for t in range(i, len(data[x])+1, i):
        color = 'C{}'.format(k)
        if z == 'Distortion Limit' and data[z][j] == 13: l = 'unlimited'
        else: l = data[z][j]
        if z == 'Stack Size':
            pl.scatter(data[x][j], data[y][j], c=color, s=20)
            pl.scatter(data[x][t-1], data[y][t-1], c=color, s=20)
            pl.plot(data[x][j+1:t-1], data[y][j+1:t-1], '-', c=color, label=l, marker='o', markersize=5)
        else: pl.plot(data[x][j:t], data[y][j:t], '-', c=color, label=l, marker='o', markersize=5)
        j = t
        k += 1
    pl.xlabel(x)
    pl.ylabel(y)
    if y == 'BLEU':
        pl.yticks(arange(int(min(data[y])), max(data[y])+.2, .4))
        i = argmax(data[y])
    else:
        pl.yticks(arange(0, max(data[y])+1, 10))
        if x == 'Distortion Limit': i = argmax([(data[y][j] if data[x][j] != 13 else 0) for j in range(len(data))])
        else: i = argmax(data[y])
        pl.legend(bbox_to_anchor=(1, 1), title=z)
    if x == 'Distortion Limit':
        ticks = [str(x) for x in range(13)]+['\u221E'] 
        pl.xticks(arange(0,14,1))
        pl.gca().set_xticklabels(ticks)
    else: pl.xticks([100,500,1000,1500,2000])
    pl.title('Max {}: {}\nat {}: {:.0f}'.format(y, data[y][i], x, data[x][i]))
    fig.set_size_inches(5, 5)
    pl.savefig('{}_vs_{}.png'.format(x, y), format='png', bbox_inches='tight')
    if draw: pl.show()
    else: pl.close()

def graph(x, y, z):
    '''creates animated plot in 3D'''
    fig = pl.figure('3D {} Plot'.format(z))
    ax = pl.subplot(projection='3d')
    ax.scatter(data[x], data[y], data[z], cmap='coolwarm', s=10, depthshade=False)
    d = array([i for i in data if i[1] not in {0,13}], dtype=typeinfo)
    fig.colorbar(ax.plot_surface(d[x].reshape(7,5), d[y].reshape(7,5), d[z].reshape(7,5), cmap='coolwarm', alpha=0.9))
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_zlabel(z)
    anim = an.FuncAnimation(fig, lambda i: ax.view_init(elev=30, azim=i), frames=360, interval=100)
    anim.save('{}anim.gif'.format(z), writer='imagemagick', fps=15)
    if draw: pl.show()
    else: pl.close()

def usage():
    print('Usage: visualise_pbresults.py --input pbbleu_file [--show-plots]')
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
    s, d, b, r = 'Stack Size', 'Distortion Limit', 'BLEU', 'Runtime (minutes)'
    typeinfo = [(s,'int'), (d, 'int'), (b, 'float'), (r, 'float')]
    data=loadtxt(ip, dtype=typeinfo, converters={1: lambda x: int(x) if int(x) != -1 else 13})
    rcParams.update({'font.size': 14})
    graph_col1vscol2(d,b,s)
    graph_col1vscol2(d,r,s)
    data.sort(order=d, kind='mergesort')
    graph_col1vscol2(s,b,d)
    graph_col1vscol2(s,r,d)
    #graph(d,s,b)
    #graph(d,s,r)
