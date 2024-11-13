import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.patches as patches

import roll_centre, gravityCenter


def line_point_angle(x0, y0, phi, x):
    return np.tan(phi)*(x-x0) + y0

def line_two_points(x1, y1, x2, y2, x):
    m = (y2-y1)/(x2-x1)
    return m*(x-x1)+y1

def line_point_slope(x0, y0, m, x):
    return m*(x-x0) + y0

def intersection(m1,x1,y1,m2,x2,y2):
    xI = (m1*x1-m2*x2+y2-y1)/(m1-m2)
    yI = m1*(xI-x1)+y1
    return xI, yI

def slope_two_points(x1, y1, x2, y2):
    return (y2-y1)/(x2-x1)

def rotation_matrix(t):
    return np.array([[np.cos(t), -np.sin(t)],[np.sin(t), np.cos(t)]])


def show_tires_tigure(roll_centre, fig, ax):
    Di, Dtw = roll_centre.D, roll_centre.Dtw
    omegaL, omegaR = roll_centre.omegaL, roll_centre.omegaR
    ht = roll_centre.ht

    # Tire figures

    # Define the coordinates of the left tire vertices
    pivotTireLeft = np.array([-Di/2, 0])
    
    verticesTireLeft = [np.matmul( rotation_matrix(omegaL), np.array([-Dtw, 0]))+ pivotTireLeft,
                        np.matmul( rotation_matrix(omegaL),np.array([Dtw, 0])) + pivotTireLeft,
                        np.matmul( rotation_matrix(omegaL),np.array([Dtw, ht]))+ pivotTireLeft,
                        np.matmul( rotation_matrix(omegaL),np.array([-Dtw, ht]))+pivotTireLeft]
    
    # Create a Polygon patch using the vertices
    tireLeft = patches.Polygon(verticesTireLeft, closed=True, edgecolor='None', facecolor='black', alpha = 0.4)
    # Add the trapezoid patch to the axis
    ax.add_patch(tireLeft)
    
    # Define the coordinates of the Right tire vertices
    pivotTireRight = np.array([Di/2, 0])
    
    verticesTireRight =  [np.matmul( rotation_matrix(omegaR), np.array([-Dtw, 0]))+ pivotTireRight,
                        np.matmul( rotation_matrix(omegaR),np.array([Dtw, 0])) + pivotTireRight,
                        np.matmul( rotation_matrix(omegaR),np.array([Dtw, ht]))+ pivotTireRight,
                        np.matmul( rotation_matrix(omegaR),np.array([-Dtw, ht]))+ pivotTireRight]
    
    # Create a Polygon patch using the vertices
    tireRight = patches.Polygon(verticesTireRight, closed=True, edgecolor='None', facecolor='black', alpha = 0.4)
    # Add the trapezoid patch to the axis
    ax.add_patch(tireRight)


def show_wishbone_chassis(pointsWishbonesTire, pointsWishbonesChasis, fig, ax):

    for X1, X2 in zip(pointsWishbonesTire, pointsWishbonesChasis):
        x=[X1[0],X2[0]]
        y=[X1[1],X2[1]]
        ax.plot(x,y, marker = 'o', markersize = 8,linewidth = 4,color = '#33C4FF')

    # Create a Polygon patch using the vertices
    chasis = [pointsWishbonesChasis[1],pointsWishbonesChasis[3],
            pointsWishbonesChasis[2], pointsWishbonesChasis[0]]
    trapezoid = patches.Polygon(chasis , closed=True, edgecolor='None', facecolor='blue', alpha = 0.2)
    # Add the trapezoid patch to the axis
    ax.add_patch(trapezoid)

def plot_intersections(roll_centre, p1, p2, fig, ax):
    """
    p1: Wishbone points in the tire
    p2: Wishbone points in the chasis
    """
    D = roll_centre.D
    slopes = [slope_two_points(p1[i,0], p1[i,1], p2[i,0], p2[i,1]) for i in range(4)]
    
    # Intersection of the wishbones LEFT lines (Iwb left)
    xIl, yIl = intersection(m1=slopes[0], x1=p1[0,0], y1=p1[0,1], m2=slopes[1], x2 = p1[1,0], y2=p1[1,1])
    
    #wishbones LEFT lines
    x1 = np.linspace(p2[0,0], xIl)
    x2 = np.linspace(p2[1,0], xIl)
    y1 = line_point_slope(x0 = p1[0,0], y0 =p1[0,1], m = slopes[0], x=x1)
    y2 = line_point_slope(x0 = p1[1,0], y0 =p1[1,1], m = slopes[1], x=x2)
    ax.plot(x1, y1, "b--")
    ax.plot(x2, y2, "b--")
    
    
    # Intersection of the wishbones RIGHT lines (Iwb RIGHT)
    xIr, yIr = intersection(m1=slopes[2], x1=p1[2,0], y1=p1[2,1], m2=slopes[3], x2 = p1[3,0], y2=p1[3,1])
    
    #wishbones RIGHT lines
    x3 = np.linspace(xIr,p2[2,0])
    x4 = np.linspace(xIr, p2[3,0])
    
    y3 = line_point_slope(x0 = p1[2,0], y0 =p1[2,1], m = slopes[2], x=x3)
    y4 = line_point_slope(x0 = p1[3,0], y0 =p1[3,1], m = slopes[3], x=x4)
    ax.plot(x3, y3, "r--")
    ax.plot(x4, y4, "r--")
    
    
    
    # Rolling Center
    ml = slope_two_points(x1 = xIl, y1 = line_point_slope(x0 = p1[0,0], y0 =p1[0,1], m = slopes[0], x=xIl), x2 = -D/2 , y2 = 0)
    mr = slope_two_points(x1 = xIr, y1 = line_point_slope(x0 = p1[3,0], y0 =p1[3,1], m = slopes[3], x=xIr), x2 = D/2 , y2 = 0)
    
    xRC, yRC = intersection(m1=ml, x1=-D/2, y1=0, m2=mr , x2 = D/2, y2=0)
    
    # Add circle to the plot
    rCenter = Circle((xRC, yRC), 0.025, fill =True,
                    label = "RC = ({} m, {} m)".format(round(xRC,3), round(yRC,3)), color = "g")
    ax.add_patch(rCenter)

    #LEFT tire position Iwg to the instantaneus center Iwb line
    xt = np.linspace(-D/2, np.max([xIl, xRC]))
    yt = line_two_points(x1 = xIl, y1 = line_point_slope(x0 = p1[0,0], y0 =p1[0,1], m = slopes[0], x=xIl), x2 = -D/2 , y2 = 0, x = xt)
    ax.plot(xt, yt, color = "g")

    #RIGHT tire position Iwg to the instantaneus center Iwb line
    xtrR = np.linspace(np.min([xIr,xRC]), D/2)
    ytr = line_two_points(x1 = xIr, y1 = line_point_slope(x0 = p1[3,0], y0 =p1[3,1], m = slopes[3], x=xIr), x2 = D/2 , y2 = 0, x = xtrR)
    ax.plot(xtrR, ytr, color = "g")

def show_center_of_gravity(center_of_gravity, fig, ax):
    cog = center_of_gravity.centreGravity()
    circle = Circle((cog[0], cog[1]), 0.025, fill =True,
                    color = "blue",
                    label ="CoG({} m, {} m)".format(round(cog[0],3), round(cog[1],3)) )
    ax.add_patch(circle)
    

            
        

    