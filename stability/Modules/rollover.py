
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from ..Modules import frontStability, chassis_stiffnes, gravityCenter

class rollover():
    def __init__(self, center_of_gravity,
                  roll_centre, max_angle, D,
                  chassis_stiffness):
        self.center_of_gravity = center_of_gravity
        self.roll_centre = roll_centre
        self.max_angle = max_angle
        self.D = D
        self.chassis_stiffness = chassis_stiffness
    
    def distance_center_of_gravity_rolling_centre(self):
        """
        Compute the distance between the Centre of gravity and roll centre
        """
        dis = self.center_of_gravity.gravity_center() - self.roll_centre
        return dis
    
    def roll_angle(self, v, R):
        """
        Compute the Roll Angle for a curve with
        Radius = R #m
        Velocity = v # km/h
        """
        v = v*0.277778 #m/s conversion
        total_mass = self.center_of_gravity.totalMass()
        centrifugal_force = total_mass*v**2/R
        vertical_distance = np.linalg.norm(self.distance_center_of_gravity_rolling_centre()[:2])
        chassis_stiffness = self.chassis_stiffness.chassis_stiffness()

        return (centrifugal_force*vertical_distance)/chassis_stiffness
    
    def max_speed_angle(self, R):
        """
        Compute the velocity for maximum angle of rotation
        Radius = R #m
        """
        max_angle = self.max_angle
        chassis_stiffness = self.chassis_stiffness.chassis_stiffness()
        total_mass = self.center_of_gravity.totalMass()
        vertical_distance = np.linalg.norm(self.distance_center_of_gravity_rolling_centre()[:2])
        return np.sqrt((max_angle*chassis_stiffness*R)/(total_mass*vertical_distance))
    
    def rotation_curve(self, R, v):
        """
        Compute the rotation of the car when is rounding a curve with
        radius R and travels in a velocity v
        Radius = R #m
        velocity = v #km/h
        """
        max_angle = self.max_angle
        chassis_stiffness = self.chassis_stiffness.chassis_stiffness()
        total_mass = self.center_of_gravity.totalMass()
        vertical_distance = np.linalg.norm(self.distance_center_of_gravity_rolling_centre()[:2])
        return (v**2*total_mass*vertical_distance)/(chassis_stiffness*R)
    
    def max_speed_weigth(self, R):
        """
        Compute the physical maximum velocity.
        The velocity in which the centrifugal toque is greater that the torque
        due to the weigth   
        Radius = R #m
        """
        g = 9.8
        d = self.D
        h = self.center_of_gravity.gravity_center()[1]
        return np.sqrt((g*d*R)/(2*h))
    
    def max_speed_weigth_modified(self, R):
        """
        Compute the physical maximum velocity but using the distance 
        between the roll center and the gravity center
        Radius = R #m
        """
        g = 9.8
        d = self.D
        vertical_distance = np.linalg.norm(self.distance_center_of_gravity_rolling_centre()[:2])
        return np.sqrt((g*d*R)/(2*vertical_distance))
    def chassisRollAngle(self):
        return
    
    def maxCurveRadious(self):
        return

        