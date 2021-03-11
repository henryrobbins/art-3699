import netpbm
import os
import time
import numpy as np
from math import ceil

import sys
sys.path.insert(1, '../')
from log import write_log

# COMPILE PIECES | 2021-03-07

# single prints

pieces = [('road_day', 8),
          ('sky', 8),           # photo taken by Ella Clemons (2/24/2021)
          ('faces', 12),        # photo taken by Ella Clemons (3/7/2021)
          ('beebe_trail', 8),
          ('stomp', 25),        # photo taken by Ella Clemons (3/7/2021)
          ('water_cup', 7)]     # photo taken by Ella Clemons (3/7/2021)

log = []  # keep track of compilation time and file sizes
for file_name, k in pieces:
    then = time.time()
    name = "%s_mod_%d" % (file_name, k)
    netpbm.convert_from_p6('mod/%s.pbm' % (file_name))
    M, w, h, n = netpbm.read('mod/%s.pgm' % (file_name))
    M_prime = np.array(list(map(lambda x: x % k, M)))
    M_prime = netpbm.enlarge(M_prime, ceil(1000 / max(M_prime.shape)))
    netpbm.write('mod/%s.pgm' % (name), M_prime, k)

    t = time.time() - then
    size = os.stat('mod/%s.pgm' % (name)).st_size
    log.append({'name':'%s.pgm' % (name), 't':'%.3f' % t, 'size':'%d' % size})

# animations

pieces = [('faces',1,150)]      # photo taken by Ella Clemons (3/7/2021)

for file_name, lb, ub in pieces:
    if not os.path.isdir('mod/%s' % file_name):
        os.mkdir('mod/%s' % file_name)
    then = time.time()
    for k in range(lb,ub+1):
        name = "%s_mod_%s" % (file_name, str(k).zfill(3))
        netpbm.convert_from_p6('mod/%s.pbm' % (file_name))
        M, w, h, n = netpbm.read('mod/%s.pgm' % (file_name))
        M_prime = np.array(list(map(lambda x: x % k, M)))
        netpbm.write('mod/%s/%s.pgm' % (file_name, name), M_prime, k)

    t = time.time() - then
    size = sum(d.stat().st_size for d in os.scandir('mod/%s' % (file_name)))
    log.append({'name':'%s' % (file_name), 't':'%.3f' % t, 'size':'%d' % size})

write_log('mod/mod.log', log)