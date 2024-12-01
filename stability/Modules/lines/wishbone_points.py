import numpy as np
from .rotation_matrix import rotationMatrix 

def wishbonePoints(object, omL=0, omR=0, theta = 0, dis1=False):
    D, Dtw = object.D, object.Dtw
    hu, hb = object.hu, object.hb
    lu, lb = object.lu, object.lb
    OmegaL, OmegaR = object.omegaL, object.omegaR

    philu = object.philu
    philb = object.philb
    phiru = object.phiru
    phirb = object.phirb
    if dis1:
        OmegaL, OmegaR = omL, omR
    else: 
        theta = object.theta
    
    cc = np.array([0, object.ycc])

    #Wishbones points
    pivotTireLeft = np.array([-D/2, 0])
    pivotTireRight = np.array([D/2, 0])
    xwl = -D/2+Dtw
    xwr = D/2-Dtw
    pointsWishbonesTire = np.array([np.matmul( rotationMatrix(OmegaL),np.array([Dtw, hu]))+ pivotTireLeft,
                            np.matmul( rotationMatrix(OmegaL),np.array([Dtw, hb]))+ pivotTireLeft,
                            np.matmul( rotationMatrix(OmegaR),np.array([-Dtw, hu]))+ pivotTireRight,
                            np.matmul( rotationMatrix(OmegaR),np.array([-Dtw, hb]))+ pivotTireRight])

    pointsWishbonesChasis = np.array([np.matmul(rotationMatrix(theta), np.array( [lu*np.sin(philu)+xwl , -lu*np.cos(philu)+hu]) -cc) + cc,
                                np.matmul(rotationMatrix(theta), np.array([lb*np.sin(philb)+xwl, lb*np.cos(philb)+hb]) -cc) + cc,
                                np.matmul(rotationMatrix(theta), np.array([-lu*np.sin(phiru)+ xwr, -lu*np.cos(phiru)+hu])-cc) + cc,
                                np.matmul(rotationMatrix(theta), np.array([-lb*np.sin(phirb)+xwr, lb*np.cos(phirb)+hb])-cc) + cc])
    t,c = pointsWishbonesTire, pointsWishbonesChasis
    ls = [lu,lb,lu,lb]
    dis = np.array([np.linalg.norm(t[i]-c[i])-l for i,l in zip(range(4),ls)])
    if dis1:
        return dis
    else:
        return pointsWishbonesTire, pointsWishbonesChasis
    
def distance(object, OmegaL, OmegaR, theta=0):
    dis = np.array([wishbonePoints(object, omL=i, omR=j, theta=theta, dis1=True) 
                    for i,j in zip(OmegaL, OmegaR)])
    return np.transpose(dis)