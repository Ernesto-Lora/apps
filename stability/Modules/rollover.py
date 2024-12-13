
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from ..Modules import frontStability, chassis_stiffnes, gravityCenter

class rollover():
    def __init__(self, center_of_gravity, total_mass,
                roll_centre, distance,
                max_angle, D,
                chassis_stiffness):
        self.center_of_gravity = center_of_gravity
        self.total_mass = total_mass
        self.roll_centre = roll_centre
        self.distance = distance
        self.max_angle = max_angle
        self.D = D
        self.chassis_stiffness = chassis_stiffness
    
    def roll_angle(self, v, R):
        """
        Compute the Roll Angle for a curve with
        Radius = R #m
        Velocity = v # km/h
        """
        v = v*0.277778 #m/s conversion
        centrifugal_force = self.total_mass*v**2/R
        chassis_stiffness = self.chassis_stiffness.chassis_stiffness()

        return (centrifugal_force*self.vertical_distance)/chassis_stiffness
    
    def max_speed_angle(self, R):
        """
        Compute the velocity for maximum angle of rotation
        Radius = R #m
        """
        max_angle = self.max_angle
        chassis_stiffness = self.chassis_stiffness.chassis_stiffness()
        return np.sqrt((max_angle*chassis_stiffness*R)/(self.total_mass*self.distance))
    
    def rotation_curve(self, R, v, distance = None):
        """
        Compute the rotation of the car when is rounding a curve with
        radius R and travels in a velocity v
        Radius = R #m
        velocity = v #km/h
        """
        chassis_stiffness = self.chassis_stiffness.chassis_stiffness()

        if (distance != None):
            vertical_distance = distance
        else:
          vertical_distance = self.distance
        print(f'The total mass is: {self.total_mass}')
        return (v**2*self.total_mass*vertical_distance)/(chassis_stiffness*R)
    
    def max_speed_weigth(self, R):
        """
        Compute the physical maximum velocity.
        The velocity in which the centrifugal toque is greater that the torque
        due to the weigth   
        Radius = R #m
        """
        g = 9.8
        d = self.D
        h = self.center_of_gravity[1]
        return np.sqrt((g*d*R)/(2*h))
    
    def max_speed_weigth_modified(self, R, distance = None):
        """
        Compute the physical maximum velocity but using the distance 
        between the roll center and the gravity center
        Radius = R #m
        """
        g = 9.8
        if (distance != None):
            vertical_distance = distance
        else:
          vertical_distance = self.distance
        d = self.D 
        return np.sqrt((g*d*R)/(2*vertical_distance))
    def chassisRollAngle(self):
        return
    
    def maxCurveRadious(self):
        return

        