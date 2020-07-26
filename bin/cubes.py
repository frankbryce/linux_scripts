#!/usr/bin/python

import math
import sys

def cube_pairs(upTo, nways=2):
    pairs = {}
    for n in range(upTo):
        nn = n+1
        if len(str(nn)[1:]) > 0 and int(str(nn)[1:]) == 0:
            print("up to: {}".format(nn))
        h = int(math.pow(nn, 1/3))+1
        for i in range(h):
            ni = i+1
            for j in range(h-ni):
                nj = j+ni+1
                if ni+nj > nn:
                    break
                if ni*ni*ni+nj*nj*nj == nn:
                    if nn not in pairs:
                        pairs[nn] = [(ni,nj)]
                    else:
                        pairs[nn].append((ni,nj))
        if nn in pairs and len(pairs[nn]) < nways:
            del pairs[nn]
        if nn in pairs:
            print(pairs)
    return pairs

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(cube_pairs(int(sys.argv[1])))
    if len(sys.argv) == 3:
        print(cube_pairs(int(sys.argv[1]),int(sys.argv[2])))
