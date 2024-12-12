import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.patches as patches
import io
import base64
import warnings

from .lines.system_object import system_object
from .lines.tires import showTiresFigure
from .lines.show_wishbones import showWishboneChasis
from .lines.show_circle import show_circle
from .lines.compute_roll_center import ComputeRollCenter
from .gravityCenter import gravity_center
from .lines.show_chassis_angle import show_chassis_angle
from .lines.show_line import show_line

def plot_system(object, gravity_center_val, fig, ax):
    showTiresFigure(object, fig, ax)
    showWishboneChasis(object, fig, ax)
    show_chassis_angle(object, fig, ax)

    roll_center = ComputeRollCenter(object)
    
    show_circle(roll_center, "green", fig, ax) #roll center
    show_circle(gravity_center_val, "blue", fig, ax) #gravity center
    show_line(roll_center, gravity_center_val, fig, ax) #Line between roll center and gravity center


class suspentionChasisSystem:
    def __init__(self, D, Dtw, ht, hu, hb, lu, lb, philu, philb, phiru, phirb):
        self.fig, self.ax = plt.subplots()
        plt.close()
        
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
        self.ComputeRollCenter()

    def get_D(self):
        return self.D 

    #def showWarning1(self): (hu>hb) The upper wishbone must be positioned above the bottom wishbone.

    #def showWarning2(self): (ht > hu and ht > hb ) The upper and bottom wishbone must be shorter than the tire diameter.

    #def showWarning3(self): (theta < max_rotation)Maximum Rotation Angle $\\theta$  has been exceeded.


    def addChassisAngle(self, theta):
        self.theta = np.deg2rad(theta)
        self.omega()
        #if not(self.war3):
            #self.showAll()


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
