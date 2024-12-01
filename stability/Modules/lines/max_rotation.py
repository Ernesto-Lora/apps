import numpy as np
from .wishbone_points import distance

def maxRotation(object):
    """
    Find the maximum rotation theta
    """
    t = np.linspace(-np.deg2rad(20), np.deg2rad(20))
    mindisL = np.min( distance(object, OmegaL=t, OmegaR=t, theta = 0)[0])
    mindisR = np.min( distance(object, OmegaL=t, OmegaR=t, theta = 0)[2])

    theta = 0
    dAng = 0.001
    while( mindisR < - 5e-3  ):
        mindisR = np.min( distance(object, OmegaL=t, OmegaR=t, theta = theta)[2])
        theta += dAng
    return theta - dAng