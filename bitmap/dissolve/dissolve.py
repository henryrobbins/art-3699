import numpy as np
import os
import time
from math import ceil
from typing import List

import sys
sys.path.insert(1, '../')
import netpbm
sys.path.insert(1, '../../')
from log import write_log


def dissolve_iter(v:np.ndarray) -> np.ndarray:
    """Return vector v after one iteration of dissolving."""
    n = len(v)
    v_new = []
    for i in range(n):
        l = 0 if i-1 < 0 else v[i-1]
        r = 0 if i+1 >= n else v[i+1]
        x = v[i]
        if x != 0:
            if (x > l) & (x > r):
                x_new = x - 2
            elif (x < l) & (x < r):
                x_new = x + 2
            elif ((x == l) & (x < r)) | ((x == r) & (x < l)):
                x_new = x + 1
            elif ((x == l) & (x > r)) | ((x == r) & (x > l)):
                x_new = x - 1
            else:
                x_new = x
        else:
            x_new = x
        v_new.append(max(0,x_new))
    return np.array(v_new)


def dissolve_vector(v:np.ndarray) -> np.ndarray:
    """Return the evolution of v as it dissolves completely."""
    n = len(v)
    v_current = v
    v_hist = [list(v)]
    while len(np.where(v_current != 0 )[0]) > 0:
        v_current = dissolve_iter(v_current)
        v_hist.append(list(v_current))
    return np.array(v_hist)


def dissolve_image(image:netpbm.Netpbm, direction:str, i:int) -> netpbm.Netpbm:
    """Dissolve the Netpbm image.

    Args:
        image (netpbm.Netpbm): Netpbm image to dissolve.
        direction (str): Direction to dissolve the image in {'h','v'}.
        int (i): Row / column index to dissolve the image from.

    Returns:
        netpbm.Netpbm: NumPy matrix representing the dissolved image.
    """
    if direction == 'h':
        M_prime = np.vstack((image.M[:i], dissolve_vector(image.M[i])))
    elif direction == 'v':
        M_prime = np.hstack((image.M[:,:i], dissolve_vector(image.M[:,i]).T))
    M_prime
    h,w = M_prime.shape
    return netpbm.Netpbm(w=w, h=h, k=image.k, M=M_prime)


# COMPILE PIECES | 2021-03-02

netpbm.convert_from_p6('beebe_trail.pbm')
image = netpbm.read('beebe_trail.pgm')
image = netpbm.change_gradient(image, 8)

pieces = [[('h',70)],
          [('h',100)],
          [('h',140)],
          [('v',80)],
          [('h',60),('v',47)],
          [('h',71),('v',251)]]

log = []  # keep track of compilation time and file sizes
for piece in pieces:
    then = time.time()
    name = ''.join([op[0] + str(op[1]) for op in piece])
    new_image = image
    for direction, i in piece:
        new_image = dissolve_image(new_image, direction, i)
    k  = ceil(1000 / max(new_image.M.shape))
    new_image = netpbm.enlarge(new_image, k)
    file_name = 'beebe_trail_%s.pgm' % (name)
    netpbm.write('%s' % (file_name), new_image)

    t = time.time() - then
    size = os.stat('%s' % (file_name)).st_size
    log.append({'name':file_name, 't':'%.3f' % t, 'size':size})

write_log('dissolve.log', log)
