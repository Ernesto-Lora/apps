import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.patches as patches

import io
import base64

import warnings

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

def rotationMatrix(t):
    return np.array([[np.cos(t), -np.sin(t)],[np.sin(t), np.cos(t)]])

import numpy as np

def my_bisection(f, a, b, tol): 
    # approximates a root, R, of f bounded 
    # by a and b to within tolerance 
    # | f(m) | < tol with m the midpoint 
    # between a and b Recursive implementation
    
    # check if a and b bound a root
    if np.sign(f(a)) == np.sign(f(b)):
        #print("No solution")
        return False
        
    # get midpoint
    m = (a + b)/2
    
    if np.abs(f(m)) < tol:
        # stopping condition, report m as root
        return m
    elif np.sign(f(a)) == np.sign(f(m)):
        # case where m is an improvement on a. 
        # Make recursive call with a = m
        return my_bisection(f, m, b, tol)
    elif np.sign(f(b)) == np.sign(f(m)):
        # case where m is an improvement on b. 
        # Make recursive call with b = m
        return my_bisection(f, a, m, tol)



class suspentionChasisSystem:
    def __init__(self, D, Dtw, ht, hu, hb, lu, lb, philu, philb, phiru, phirb):
        self.war1 = False
        self.war2 = False
        self.war3 = False
        self.fig, self.ax = plt.subplots()
        plt.close()

        #Geometric conditions
        if (hb>hu):
            self.war1 = True
            self.showWarning1()
            
        
        if (hu>ht or hb>ht):
            self.war2 = True
            self.showWarning2()
        
        self.D = D
        self.Dtw = Dtw
        self.ht = ht
        self.hu = hu
        self.hb = hb
        self.lu = lu
        self.lb = lb
        self.philu = np.deg2rad(philu)
        self.philb = np.deg2rad(philb) 
        self.phiru = np.deg2rad(phiru)
        self.phirb = np.deg2rad(phirb)

        self.ycc = (hu-lu*np.cos(self.phiru)+hb+lb*np.cos(self.phirb))/2

        self.theta = 0
        self.omegaR = 0
        self.omegaL = 0
        
        self.cog = 0
        self.gravity = False

        self.rollCenter = np.array([])
        self.ComputeRollCenter()

    def get_D(self):
        return self.D 

    #def showWarning1(self): The upper wishbone must be \n positioned above the bottom wishbone.

    #def showWarning2(self): The upper and bottom wishbone must be shorter than the tire diameter.

    #def showWarning3(self): Maximum Rotation Angle $\\theta$  has been exceeded.

    def ComputeRollCenter(self):
        """
        p1: Wishbone points in the tire
        p2: Wishbone points in the chasis
        """
        p1, p2 = self.wishbonePoints()
        D = self.D
        slopes = [slopeTwoPoints(p1[i,0], p1[i,1], p2[i,0], p2[i,1]) for i in range(4)]
        
        # Intersection of the wishbones LEFT lines (Iwb left)
        xIl, yIl = intersection(m1=slopes[0], x1=p1[0,0], y1=p1[0,1], m2=slopes[1], x2 = p1[1,0], y2=p1[1,1])
        
        # Intersection of the wishbones RIGHT lines (Iwb RIGHT)
        xIr, yIr = intersection(m1=slopes[2], x1=p1[2,0], y1=p1[2,1], m2=slopes[3], x2 = p1[3,0], y2=p1[3,1])
        
        # Rolling Center
        ml = slopeTwoPoints(x1 = xIl, y1 = linePointSlope(x0 = p1[0,0], y0 =p1[0,1], m = slopes[0], x=xIl), x2 = -D/2 , y2 = 0)
        mr = slopeTwoPoints(x1 = xIr, y1 = linePointSlope(x0 = p1[3,0], y0 =p1[3,1], m = slopes[3], x=xIr), x2 = D/2 , y2 = 0)
        
        xRC, yRC = intersection(m1=ml, x1=-D/2, y1=0, m2=mr , x2 = D/2, y2=0)

        self.rollCenter = np.array([xRC, yRC, 0])

    def getRollCenter(self):
        return self.rollCenter


    def addChassisAngle(self, theta):
        self.theta = np.deg2rad(theta)
        self.omega()
        #if not(self.war3):
            #self.showAll()
        

    def showTiresFigure(self):
        Di, Dtw, ht, OmegaL, OmegaR=self.D, self.Dtw, self.ht, self.omegaL, self.omegaR
        # Tire figures
    
        # Define the coordinates of the left tire vertices
        pivotTireLeft = np.array([-Di/2, 0])
        
        verticesTireLeft = [np.matmul( rotationMatrix(OmegaL), np.array([-Dtw, 0]))+ pivotTireLeft,
                            np.matmul( rotationMatrix(OmegaL),np.array([Dtw, 0])) + pivotTireLeft,
                            np.matmul( rotationMatrix(OmegaL),np.array([Dtw, ht]))+ pivotTireLeft,
                            np.matmul( rotationMatrix(OmegaL),np.array([-Dtw, ht]))+pivotTireLeft]
        
        # Create a Polygon patch using the vertices
        tireLeft = patches.Polygon(verticesTireLeft, closed=True, edgecolor='None', facecolor='black', alpha = 0.4)
        # Add the trapezoid patch to the axis
        self.ax.add_patch(tireLeft)
        
        # Define the coordinates of the Right tire vertices
        pivotTireRight = np.array([Di/2, 0])
        
        verticesTireRight =  [np.matmul( rotationMatrix(OmegaR), np.array([-Dtw, 0]))+ pivotTireRight,
                            np.matmul( rotationMatrix(OmegaR),np.array([Dtw, 0])) + pivotTireRight,
                            np.matmul( rotationMatrix(OmegaR),np.array([Dtw, ht]))+ pivotTireRight,
                            np.matmul( rotationMatrix(OmegaR),np.array([-Dtw, ht]))+ pivotTireRight]
        
        # Create a Polygon patch using the vertices
        tireRight = patches.Polygon(verticesTireRight, closed=True, edgecolor='None', facecolor='black', alpha = 0.4)
        # Add the trapezoid patch to the axis
        self.ax.add_patch(tireRight)

    def wishbonePoints(self, omL=0, omR=0, theta = 0, dis1=False):
        D, Dtw = self.D, self.Dtw
        hu, hb = self.hu, self.hb
        lu, lb = self.lu, self.lb
        OmegaL, OmegaR = self.omegaL, self.omegaR

        philu = self.philu
        philb = self.philb
        phiru = self.phiru
        phirb = self.phirb
        if dis1:
            OmegaL, OmegaR = omL, omR
        
        cc = np.array([0, self.ycc])

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
        
    def distance(self, OmegaL, OmegaR, theta=0):
        dis = np.array([self.wishbonePoints(omL=i, omR=j, theta=theta, dis1=True) for i,j in zip(OmegaL, OmegaR)])
        return np.transpose(dis)
    
    def maxRotation(self):
        """
        Find the maximum rotation theta
        """
        t = np.linspace(-np.deg2rad(20), np.deg2rad(20))
        mindisL = np.min( self.distance(OmegaL=t, OmegaR=t, theta = 0)[0])
        mindisR = np.min( self.distance(OmegaL=t, OmegaR=t, theta = 0)[2])

        theta = 0
        dAng = 0.001
        while( mindisR < - 5e-3  ):
            mindisR = np.min( self.distance(OmegaL=t, OmegaR=t, theta = theta)[2])
            #print(mindisR)
            theta += dAng
        return theta - dAng



    
    def omega(self):
        """
        Modify the values of self.omegaL and self.omegaR 
        according to the current value of self.theta
        """
        # we will find the minimum value because it help us to find the solution
        t = np.linspace(-np.deg2rad(20), np.deg2rad(20))
        dis = self.distance(OmegaL=t, OmegaR=t, theta = self.theta)
        omL_min =t[np.argmin(dis[0])]
        omR_min = t[np.argmin(dis[3])]

        fL = lambda om: self.wishbonePoints(omL=om, omR=0, theta = self.theta, dis1=True)[0]
        fR = lambda om: self.wishbonePoints(omL=0, omR=om, theta = self.theta, dis1=True)[2]

        #Left
        omL = my_bisection(fL, a=omL_min, b=0.1, tol=1e-6)
        #Right
        omR = my_bisection(fR, a=-0.1, b=omR_min, tol=1e-6)

        if (omL==False or omR==False):
            self.showWarning3()
            self.war3 = True
            self.theta = 0
            self.omegaL = 0
            self.omegaR = 0
        else:
            self.war3 = False
            self.omegaL = omL
            self.omegaR = omR

    
    def showWishboneChasis(self, pointsWishbonesTire, pointsWishbonesChasis):
    
        for X1, X2 in zip(pointsWishbonesTire, pointsWishbonesChasis):
            x=[X1[0],X2[0]]
            y=[X1[1],X2[1]]
            self.ax.plot(x,y, marker = 'o', markersize = 8,linewidth = 4,color = '#33C4FF')
    
        # Create a Polygon patch using the vertices
        chasis = [pointsWishbonesChasis[1],pointsWishbonesChasis[3],
                 pointsWishbonesChasis[2], pointsWishbonesChasis[0]]
        trapezoid = patches.Polygon(chasis , closed=True, edgecolor='None', facecolor='blue', alpha = 0.2)
        # Add the trapezoid patch to the axis
        self.ax.add_patch(trapezoid)

    def plotIntersections(self, p1, p2):
        """
        p1: Wishbone points in the tire
        p2: Wishbone points in the chasis
        """
        D = self.D
        slopes = [slopeTwoPoints(p1[i,0], p1[i,1], p2[i,0], p2[i,1]) for i in range(4)]
        
        # Intersection of the wishbones LEFT lines (Iwb left)
        xIl, yIl = intersection(m1=slopes[0], x1=p1[0,0], y1=p1[0,1], m2=slopes[1], x2 = p1[1,0], y2=p1[1,1])
        
        #wishbones LEFT lines
        x1 = np.linspace(p2[0,0], xIl)
        x2 = np.linspace(p2[1,0], xIl)
        y1 = linePointSlope(x0 = p1[0,0], y0 =p1[0,1], m = slopes[0], x=x1)
        y2 = linePointSlope(x0 = p1[1,0], y0 =p1[1,1], m = slopes[1], x=x2)
        self.ax.plot(x1, y1, "b--")
        self.ax.plot(x2, y2, "b--")
        
        
        # Intersection of the wishbones RIGHT lines (Iwb RIGHT)
        xIr, yIr = intersection(m1=slopes[2], x1=p1[2,0], y1=p1[2,1], m2=slopes[3], x2 = p1[3,0], y2=p1[3,1])
        
        #wishbones RIGHT lines
        x3 = np.linspace(xIr,p2[2,0])
        x4 = np.linspace(xIr, p2[3,0])
        
        y3 = linePointSlope(x0 = p1[2,0], y0 =p1[2,1], m = slopes[2], x=x3)
        y4 = linePointSlope(x0 = p1[3,0], y0 =p1[3,1], m = slopes[3], x=x4)
        self.ax.plot(x3, y3, "r--")
        self.ax.plot(x4, y4, "r--")
        
        
        
        # Rolling Center
        ml = slopeTwoPoints(x1 = xIl, y1 = linePointSlope(x0 = p1[0,0], y0 =p1[0,1], m = slopes[0], x=xIl), x2 = -D/2 , y2 = 0)
        mr = slopeTwoPoints(x1 = xIr, y1 = linePointSlope(x0 = p1[3,0], y0 =p1[3,1], m = slopes[3], x=xIr), x2 = D/2 , y2 = 0)
        
        xRC, yRC = intersection(m1=ml, x1=-D/2, y1=0, m2=mr , x2 = D/2, y2=0)
        
        # Add circle to the plot
        rCenter = Circle((xRC, yRC), 0.025, fill =True,
                        label = "RC = ({} m, {} m)".format(round(xRC,3), round(yRC,3)), color = "g")
        self.ax.add_patch(rCenter)

        #LEFT tire position Iwg to the instantaneus center Iwb line
        xt = np.linspace(-D/2, np.max([xIl, xRC]))
        yt = lineTwoPoints(x1 = xIl, y1 = linePointSlope(x0 = p1[0,0], y0 =p1[0,1], m = slopes[0], x=xIl), x2 = -D/2 , y2 = 0, x = xt)
        self.ax.plot(xt, yt, color = "g")

        #RIGHT tire position Iwg to the instantaneus center Iwb line
        xtrR = np.linspace(np.min([xIr,xRC]), D/2)
        ytr = lineTwoPoints(x1 = xIr, y1 = linePointSlope(x0 = p1[3,0], y0 =p1[3,1], m = slopes[3], x=xIr), x2 = D/2 , y2 = 0, x = xtrR)
        self.ax.plot(xtrR, ytr, color = "g")

    def plot_roll_center(self):
        xRC, yRC, z = self.rollCenter
        # Add circle to the plot
        rCenter = Circle((xRC, yRC), 0.025, fill =True, color = "green")
        self.ax.add_patch(rCenter)


    def addCenterGravity(self, cog):
        self.cog = cog
        self.gravity = True
    
    def showCenterGravity(self):
        circle = Circle((self.cog[0], self.cog[1]), 0.025, fill =True,
                         color = "blue")
        self.ax.add_patch(circle)

    def show_chassis_angle(self):
        # Define parameters for the angle and limits
        theta = self.theta  # angle in radians, replace with your value
        line_length = 0.5  # adjust based on the plot scale

        # Add the red dashed line indicating the angle θ
        x_end = line_length * np.cos(theta)
        y_end = self.ycc + line_length * np.sin(theta)
        self.ax.plot([0, x_end], [self.ycc, y_end], 'r--', label=r'$\theta$')  # Red dashed line for angle

        # Add a horizontal reference line (optional based on your image)
        self.ax.plot([-0.3*self.D, 0.3*self.D], [self.ycc, self.ycc], color='red', linewidth=1)




    def showAll(self):
        if not(self.war3):
            self.fig, self.ax = plt.subplots(figsize=(6, 3))
            p1, p2 = self.wishbonePoints(theta=self.theta)

            self.showWishboneChasis(pointsWishbonesTire=p1, pointsWishbonesChasis=p2)
            self.showTiresFigure()
            if self.gravity == True:
                self.showCenterGravity()
            self.plot_roll_center()
            self.show_chassis_angle()
            plt.gca().set_aspect('equal', adjustable='box')
            plt.ylim(-0.1, 0.7)
            plt.xlim(-1.2, 1.2)
            plt.legend()
            
            # Save the plot to a BytesIO object
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            
            # Convert to base64 for embedding in HTML
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            buffer.close()
            return image_base64
    

            
        

    