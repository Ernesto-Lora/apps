import numpy as np
from .bisection import bisection
from .wishbone_points import distance, wishbonePoints

def omega(object):
    """
    Modify the values of object.omegaL and object.omegaR 
    according to the current value of object.theta
    """
    # we will find the minimum value because it help us to find the solution
    t = np.linspace(-np.deg2rad(20), np.deg2rad(20))
    dis = distance(object, OmegaL=t, OmegaR=t, theta = object.theta)
    omL_min =t[np.argmin(dis[0])]
    omR_min = t[np.argmin(dis[3])]

    fL = lambda om: wishbonePoints(object, omL=om, omR=0, theta = object.theta, dis1=True)[0]
    fR = lambda om: wishbonePoints(object, omL=0, omR=om, theta = object.theta, dis1=True)[2]

    #Left
    omL = bisection(fL, a=omL_min, b=0.1, tol=1e-6)
    #Right
    omR = bisection(fR, a=-0.1, b=omR_min, tol=1e-6)

    if (omL==False or omR==False):
        # Warning3
        object.theta = 0
        object.omegaL = 0
        object.omegaR = 0
    else:
        object.omegaL = omL
        object.omegaR = omR