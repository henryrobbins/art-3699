import numpy as np
from dmtools import netpbm
import logging
logging.basicConfig(filename='clip.log',
                    level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%m-%d-%Y %I:%M')

def clip(image:netpbm.Netpbm,
         k:int, lb:int, ub:int, b:int, c:str) -> netpbm.Netpbm:
    """Return the Netpbm image mod k.

    Args:
        image (netpbm.Netpbm): Netpbm image to mod.
        k (int): Number of gradients.
        lb (int): Lower bound of gradients to show.
        ub (int): Upper bound of gradients to show.
        b (int): Width of the border.
        c (str): Color of the border {'white', 'black'}

    Returns:
        netpbm.Netpbm: NumPy matrix representing the mod image.
    """
    image = netpbm.change_gradient(image, k)
    h,w = image.M.shape
    M_lb = np.where(lb <= image.M, 1, 0)
    M_ub = np.where(image.M <= ub, 1, 0)
    M = np.where(M_lb + M_ub == 2, 0, 1)
    image = netpbm.Netpbm(P=image.P, w=w, h=h, k=1, M=M)
    return netpbm.border(image, b, c)


# COMPILE PIECES | 2021-03-23

# single prints

pieces = [('beebe_trail', 8, 0, 0, 75, "black"),
          ('road_day', 8, 0, 0, 75, "black"),
          ('creek', 8, 0, 0, 75, "black"),
          ('tree_light', 8, 1, 2, 75, "black"),
          ('buildings_night', 8, 2, 3, 75, "black"),
          ('porch', 8, 4, 8, 75, "black"),
          ('wall_light', 8, 5, 6, 75, "black"),
          ('laundry', 8, 0, 1, 75, "black")]

works = []
for name, k, lb, ub, b, c in pieces:
    file_path = "%s_clip_%d_%d.pgm" % (name, lb, ub)
    ppm_path = '%s.ppm' % name
    netpbm.transform(in_path=ppm_path, out_path=file_path,
                     magic_number=2, f=clip, k=k, lb=lb, ub=ub, b=b,
                     c=c, scale=1000)
    works.append("%s_clip_%d_%d.pgm" % (name, lb, ub))

with open("works.txt", "w") as f:
    for work in works:
        f.write("%s\n" % work)
