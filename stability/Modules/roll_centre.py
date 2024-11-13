import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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



class roll_centre:
    def __init__(self, D, Dtw, ht, hu, hb, lu, lb, philu, philb, phiru, phirb):
        self.war1 = False
        self.war2 = False
        self.war3 = False

        #Geometric conditions
        if (hb>hu):
            self.war1 = True
            #self.showWarning1()
            
        
        if (hu>ht or hb>ht):
            self.war2 = True
            #self.showWarning2()
        
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

        self.rollCenter = np.array([])
        self.calculate_roll_centre()

    def get_D(self):
        return self.D 

    def showWarning1(self):
        self.fig, self.ax = plt.subplots()
        # Add text in the center
        self.ax.text(0.5, 0.8, 'Warning!', horizontalalignment='center', verticalalignment='center', fontsize=32)
        self.ax.text(0.5, 0.60, 'Error: The upper wishbone must be \n positioned above the bottom wishbone.',
                horizontalalignment='center', verticalalignment='center', fontsize=24)
        self.ax.text(0.5, 0.40, 'Please enter values such that $h_u > h_b$',
                horizontalalignment='center', verticalalignment='center', fontsize=24)
        # Set axis limits
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

        # Hide axes
        self.ax.axis('off')

        plt.show()

    def showWarning2(self):
        self.fig, self.ax = plt.subplots()
        # Add text in the center
        self.ax.text(0.5, 0.8, 'Warning!', horizontalalignment='center', verticalalignment='center', fontsize=32)
        self.ax.text(0.5, 0.60, 'Error: The upper and bottom wishbone\n must be shorter than the tire diameter.',
                horizontalalignment='center', verticalalignment='center', fontsize=24)
        self.ax.text(0.5, 0.40, 'Please enter values such that\n $h_u < h_t$ and $h_b < h_t$',
                horizontalalignment='center', verticalalignment='center', fontsize=24)
        # Set axis limits
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

        # Hide axes
        self.ax.axis('off')

        plt.show()

    def showWarning3(self):
        self.fig, self.ax = plt.subplots()
        # Add text in the center
        self.ax.text(0.5, 0.8, 'Warning!', horizontalalignment='center', verticalalignment='center', fontsize=32)
        self.ax.text(0.5, 0.60, "Maximum Rotation Angle $\\theta$ has been exceeded.\n Please enter a smaller angle or adjust the geometry.",
                horizontalalignment='center', verticalalignment='center', fontsize=24)
        
        # Set axis limits
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

        # Hide axes
        self.ax.axis('off')

        plt.show()

    def wishbone_points(self, omegaL = 0, omegaR=0, theta = 0):
        D, Dtw = self.D, self.Dtw
        hu, hb = self.hu, self.hb
        lu, lb = self.lu, self.lb
        #omegaL, omegaR = self.omegaL, self.omegaR

        philu = self.philu
        philb = self.philb
        phiru = self.phiru
        phirb = self.phirb
        
        cc = np.array([0, self.ycc])

        #Wishbones points
        pivot_tire_left = np.array([-D/2, 0])
        pivot_tire_right = np.array([D/2, 0])
        xwl = -D/2+Dtw
        xwr = D/2-Dtw
        points_wishbones_tire = np.array([np.matmul( rotation_matrix(omegaL),np.array([Dtw, hu]))+ pivot_tire_left,
                              np.matmul( rotation_matrix(omegaL),np.array([Dtw, hb]))+ pivot_tire_left,
                              np.matmul( rotation_matrix(omegaR),np.array([-Dtw, hu]))+ pivot_tire_right,
                              np.matmul( rotation_matrix(omegaR),np.array([-Dtw, hb]))+ pivot_tire_right])
    
        points_wishbones_chassis = np.array([np.matmul(rotation_matrix(theta), np.array( [lu*np.sin(philu)+xwl , -lu*np.cos(philu)+hu]) -cc) + cc,
                                 np.matmul(rotation_matrix(theta), np.array([lb*np.sin(philb)+xwl, lb*np.cos(philb)+hb]) -cc) + cc,
                                 np.matmul(rotation_matrix(theta), np.array([-lu*np.sin(phiru)+ xwr, -lu*np.cos(phiru)+hu])-cc) + cc,
                                 np.matmul(rotation_matrix(theta), np.array([-lb*np.sin(phirb)+xwr, lb*np.cos(phirb)+hb])-cc) + cc])
        
        return points_wishbones_tire, points_wishbones_chassis
    
    def distance_between_tire_chassis(self, omegaL = 0, omegaR=0, theta = 0):
        #print(omegaL)
        p1, p2 = self.wishbone_points(omegaL = omegaL, omegaR=omegaR, theta = theta)
        lengths = [self.lu,self.lb,self.lu,self.lb]
        return np.array([np.linalg.norm(p1[i]-p2[i])-l for i,l in zip(range(4), lengths)])

    def distance_multiple_omegas(self, theta=0):
        omega_array = np.linspace(-np.deg2rad(25), np.deg2rad(25))
        return np.transpose( np.array([self.distance_between_tire_chassis(omegaL=omL, omegaR=omR, theta=theta) 
                        for omL, omR in zip(omega_array, omega_array)]))
    
    def max_rotation(self):
        """
        Find the maximum rotation theta
        """
        mindisR = np.min(self.distance_multiple_omegas(theta = 0)[2])
        theta = 0
        dAng = 0.001

        while( mindisR < - 5e-3  ):
            mindisR = np.min(self.distance_multiple_omegas(theta = theta)[2])
            theta += dAng
        return theta - dAng
    
    def omega(self):
        """
        Modify the values of self.omegaL and self.omegaR 
        according to the current value of self.theta
        """
        # we will find the minimum value because it help us to find the solution
        omega_array = np.linspace(-np.deg2rad(25), np.deg2rad(25))
        dis = self.distance_multiple_omegas(theta = self.theta)
        omL_min = omega_array[np.argmin(dis[0])]
        omR_min = omega_array[np.argmin(dis[3])]

        fL = lambda om: self.distance_between_tire_chassis(omegaL=om, omegaR=0, theta = self.theta)[0]
        fR = lambda om: self.distance_between_tire_chassis(omegaL=0, omegaR=om, theta = self.theta)[2]

        #Left
        omL = my_bisection(fL, a=omL_min, b=0.1, tol=1e-6)
        #Right
        omR = my_bisection(fR, a=-0.1, b=omR_min, tol=1e-6)

        if (omL==False or omR==False):
            #self.showWarning3()
            self.war3 = True
            self.theta = 0
            self.omegaL = 0
            self.omegaR = 0
        else:
            self.war3 = False
            self.omegaL = omL
            self.omegaR = omR



    def calculate_roll_centre(self):
        """
        p1: Wishbone points in the tire
        p2: Wishbone points in the chasis
        """
        p1, p2 = self.wishbone_points()
        D = self.D
        slopes = [slope_two_points(p1[i,0], p1[i,1], p2[i,0], p2[i,1]) for i in range(4)]
        
        # Intersection of the wishbones LEFT lines (Iwb left)
        xIl, yIl = intersection(m1=slopes[0], x1=p1[0,0], y1=p1[0,1], m2=slopes[1], x2 = p1[1,0], y2=p1[1,1])
        
        # Intersection of the wishbones RIGHT lines (Iwb RIGHT)
        xIr, yIr = intersection(m1=slopes[2], x1=p1[2,0], y1=p1[2,1], m2=slopes[3], x2 = p1[3,0], y2=p1[3,1])
        
        # Rolling Center
        ml = slope_two_points(x1 = xIl, y1 = line_point_slope(x0 = p1[0,0], y0 =p1[0,1], m = slopes[0], x=xIl), x2 = -D/2 , y2 = 0)
        mr = slope_two_points(x1 = xIr, y1 = line_point_slope(x0 = p1[3,0], y0 =p1[3,1], m = slopes[3], x=xIr), x2 = D/2 , y2 = 0)
        
        xRC, yRC = intersection(m1=ml, x1=-D/2, y1=0, m2=mr , x2 = D/2, y2=0)

        self.rollCenter = np.array([xRC, yRC, 0])

    def get_roll_center(self):
        return self.rollCenter


    def add_chassis_angle(self, theta):
        self.theta = np.deg2rad(theta)
        self.omega()
        
        

    