import numpy as np

def linePointAngle(x0, y0, phi, x):
    return np.tan(phi)*(x-x0) + y0

def lineTwoPoints(x1, y1, x2, y2, x):
    m = (y2-y1)/(x2-x1)
    return m*(x-x1)+y1

def linePointSlope(x0, y0, m, x):
    return m*(x-x0) + y0

def intersection(m1,x1,y1,m2,x2,y2):
    xI = (m1*x1-m2*x2+y2-y1)/(m1-m2)
    yI = m1*(xI-x1)+y1
    return xI, yI

def slopeTwoPoints(x1, y1, x2, y2):
    return (y2-y1)/(x2-x1)