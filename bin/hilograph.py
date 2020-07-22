#!/usr/bin/python

import hilo
import numpy as np
from PIL import Image
import sys

def hilograph(n):
    data = np.zeros((n,n,3), dtype=np.uint8)
    for i in range(n):
        _,g = hilo.hilo(i+1)
        for gi in g:
            data[i,gi] = [254,0,0]
    img = Image.fromarray(data)
    img.save("hilograph{}.bmp".format(n))

if __name__ == "__main__":
  hilograph(int(sys.argv[1]))
