#!/bin/env/python3
#Author: Saurabh Pathak
import data
from sys import stderr

def construct(chunkset, line, l, verbose=False):
    #knapsack problem instance
    if verbose: print('Recombining segments...', sep='', end='', flush=True, file=stderr)
    dp = [[None]*(l+1) for i in range(l+1)]

    def knapsack(istart, iend):
        if istart == iend: return 0, ''
        if dp[istart][iend] is not None: return dp[istart][iend]
        maxcost, span = 0, ' '.join(line[istart:iend])
        for chunk in chunkset:
            if chunk.istart >= istart and chunk.iend <= iend:
                leftcost, leftspan = knapsack(istart, chunk.istart)
                rightcost, rightspan = knapsack(chunk.iend, iend)
                cost = leftcost + (chunk.iend-chunk.istart)**2  + rightcost
                if cost > maxcost:
                    maxcost = cost
                    span = leftspan + '<xml translation="{}" prob=0.6>{}</xml>'.format(' '.join(data.e[chunk.segid].split()[chunk.start:chunk.end]) if isinstance(chunk, data._Match) else chunk.trans, ' '.join(line[chunk.istart:chunk.iend]))  + rightspan
        dp[istart][iend] = maxcost, span
        return maxcost, span

    xml = knapsack(0, l)[1]
    if verbose: print('Done', flush=True, file=stderr)
    return xml
