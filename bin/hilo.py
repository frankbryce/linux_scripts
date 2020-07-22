#!/usr/bin/python

import sys
import functools

@functools.lru_cache(maxsize=None)
def hilo(n):
    if n<1:
        raise Exception("n must be >= 1")
    if n==1:
        return 1.0,[1]
    if n==2:
        return 1.5,[1,2]
    minE = n+1
    minG = []
    for i in range(n):
        le,re = 0.0,0.0
        if i+1 > 1:
            le,_ = hilo(i)
        if i+1 < n:
            re,_ = hilo(n-(i+1))
        e=le*float(i)/n+re*float(n-i-1)/n+1.0
        if minE > e:
            minE = e
            minG = [i+1]
        elif minE == e:
            minG.append(i+1)
    return minE,minG


if __name__ == "__main__":
    print(hilo(int(sys.argv[1])))
