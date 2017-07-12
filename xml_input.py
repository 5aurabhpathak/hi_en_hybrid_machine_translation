#!/bin/env/python3
#Author: Saurabh Pathak
import data, rulebaseprior
from sys import stderr

def construct(chunkset, line, l, tags, verbose=False):
    return ' '.join(line) #uncomment this to disable EBMT, RBMT and splitting constraints
    if verbose: print('Recombining segments...', sep='', end='', flush=True, file=stderr)
    #Avoiding malformed xml
    temp = []
    for chunk in chunkset:
        if isinstance(chunk, data._Match):
            chunk.trans = ' '.join(data.e[chunk.segid].split()[chunk.start:chunk.end]).strip('"<>/')
            if len(chunk.trans) == 0: continue
            if chunk.iend-chunk.istart == 1 and tags[chunk.istart]['coarsePOS'] != 'n' and tags[chunk.istart]['POS'] != 'VM': continue
        temp.append(chunk)
    chunkset = temp

    #knapsack problem instance
    dp = [[None]*(l+1) for i in range(l+1)]

    def knapsack(istart, iend):
        if istart == iend: return 0, ''
        if dp[istart][iend] is not None: return dp[istart][iend]
        maxcost = 0
        span = rulebaseprior.add_walls(istart, iend, tags, l, line) #Comment this line and uncomment following line to disable reordering constarints
        #span = ' '.join(line[istart:iend])
        for chunk in chunkset:
            if chunk.istart >= istart and chunk.iend <= iend:
                leftcost, leftspan = knapsack(istart, chunk.istart)
                rightcost, rightspan = knapsack(chunk.iend, iend)
                cost = leftcost + ((chunk.iend-chunk.istart)**2)*chunk.fms  + rightcost
                if cost > maxcost:
                    maxcost = cost
                    span = ' '.join([leftspan, '<xml translation="{}" prob="{}">{}</xml>'.format(chunk.trans, chunk.fms, ' '.join(line[chunk.istart:chunk.iend])), rightspan])
        dp[istart][iend] = maxcost, span
        return maxcost, span

    rulebaseprior.wall = False
    xml = knapsack(0, l)[1]
    if verbose: print('Done', flush=True, file=stderr)
    #if rulebaseprior.wall: return xml.split('<wall />')
    return xml
