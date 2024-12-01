import numpy as np
import matplotlib.patches as patches
from .rotation_matrix import rotationMatrix

def showTiresFigure(object, fig, ax):
    Di = object.D
    Dtw = object.Dtw
    ht = object.ht
    OmegaL = object.omegaL
    OmegaR = object.omegaR

    # Define the coordinates of the left tire vertices
    pivotTireLeft = np.array([-Di/2, 0])
    
    verticesTireLeft = [np.matmul( rotationMatrix(OmegaL), np.array([-Dtw, 0]))+ pivotTireLeft,
                        np.matmul( rotationMatrix(OmegaL),np.array([Dtw, 0])) + pivotTireLeft,
                        np.matmul( rotationMatrix(OmegaL),np.array([Dtw, ht]))+ pivotTireLeft,
                        np.matmul( rotationMatrix(OmegaL),np.array([-Dtw, ht]))+pivotTireLeft]
    
    # Create a Polygon patch using the vertices
    tireLeft = patches.Polygon(verticesTireLeft, closed=True, edgecolor='None', facecolor='black', alpha = 0.4)
    # Add the trapezoid patch to the axis
    ax.add_patch(tireLeft)
    
    # Define the coordinates of the Right tire vertices
    pivotTireRight = np.array([Di/2, 0])
    
    verticesTireRight =  [np.matmul( rotationMatrix(OmegaR), np.array([-Dtw, 0]))+ pivotTireRight,
                        np.matmul( rotationMatrix(OmegaR),np.array([Dtw, 0])) + pivotTireRight,
                        np.matmul( rotationMatrix(OmegaR),np.array([Dtw, ht]))+ pivotTireRight,
                        np.matmul( rotationMatrix(OmegaR),np.array([-Dtw, ht]))+ pivotTireRight]
    
    # Create a Polygon patch using the vertices
    tireRight = patches.Polygon(verticesTireRight, closed=True, edgecolor='None', facecolor='black', alpha = 0.4)
    # Add the trapezoid patch to the axis
    ax.add_patch(tireRight)