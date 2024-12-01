import numpy as np
from .lines import slopeTwoPoints, intersection, linePointSlope
from .wishbone_points import wishbonePoints
def ComputeRollCenter(object):
        """
        p1: Wishbone points in the tire
        p2: Wishbone points in the chasis
        """
        p1, p2 = wishbonePoints(object)
        D = object.D
        slopes = [slopeTwoPoints(p1[i,0], p1[i,1], p2[i,0], p2[i,1]) for i in range(4)]
        
        # Intersection of the wishbones LEFT lines (Iwb left)
        xIl, yIl = intersection(m1=slopes[0], x1=p1[0,0], y1=p1[0,1], m2=slopes[1], x2 = p1[1,0], y2=p1[1,1])
        
        # Intersection of the wishbones RIGHT lines (Iwb RIGHT)
        xIr, yIr = intersection(m1=slopes[2], x1=p1[2,0], y1=p1[2,1], m2=slopes[3], x2 = p1[3,0], y2=p1[3,1])
        
        # Rolling Center
        ml = slopeTwoPoints(x1 = xIl, y1 = linePointSlope(x0 = p1[0,0], y0 =p1[0,1], m = slopes[0], x=xIl), x2 = -D/2 , y2 = 0)
        mr = slopeTwoPoints(x1 = xIr, y1 = linePointSlope(x0 = p1[3,0], y0 =p1[3,1], m = slopes[3], x=xIr), x2 = D/2 , y2 = 0)
        
        xRC, yRC = intersection(m1=ml, x1=-D/2, y1=0, m2=mr , x2 = D/2, y2=0)

        return np.array([xRC, yRC, 0])