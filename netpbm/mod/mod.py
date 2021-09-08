import numpy as np
from dmtools import netpbm
from dmtools import colorspace
from dmtools.animation import animation
import logging
logging.basicConfig(filename='mod.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')


def mod(image:netpbm.Netpbm, k:int) -> netpbm.Netpbm:
    """Return the Netpbm image mod k.

    Args:
        image (netpbm.Netpbm): Netpbm image to mod.
        k (int): Integer to mod the image by

    Returns:
        netpbm.Netpbm: NumPy matrix representing the mod image.
    """
    M_prime = colorspace.RGB_to_gray(image.M)
    M_prime = np.array(list(map(lambda x: x % k, M_prime)))
    return netpbm.Netpbm(P=2, k=k, M=M_prime)


# COMPILE PIECES | 2021-03-07

# single prints

pieces = [('road_day', 8),
          ('sky', 8),
          ('faces', 12),
          ('beebe_trail', 8),
          ('stomp', 25),
          ('water_cup', 7)]

works = []
for name, k in pieces:
    image = netpbm.read_netpbm('%s.ppm' % name)
    image = mod(image, k)
    path = "%s_mod_%d.pgm" % (name, k)
    image.to_netpbm(path)
    works.append(path)

# animations

pieces = [('faces',1,150),
          ('water_cup',1,140)]

for name, lb, ub in pieces:
    image = netpbm.read_netpbm('%s.ppm' % name)
    frames = [mod(image,k).M * (255/k) for k in range(lb,ub+1)]
    path = '%s_mod_animation.mp4' % name
    animation(frames=frames, path=path, fps=10, s=4)
    works.append(path)

with open("works.txt", "w") as f:
    for work in works:
        f.write("%s\n" % work)
