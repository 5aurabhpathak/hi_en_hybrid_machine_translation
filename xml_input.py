#!/bin/env/python3
#Author: Saurabh Pathak
import data

def construct(chunkset, line, l):
    #knapsack problem instance
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

    return knapsack(0, l)[1]

