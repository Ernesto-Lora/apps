import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class gravity_center:
    def __init__(self, components = pd.DataFrame()):
        """
        Compute the center of gravity from a dataframe with component positions and weights.
        Parameters:
        df (pd.DataFrame): DataFrame with columns 
        ["component_name", "mass", "x", "y", "z"]
        """
        self.components = components

    def addComponents(self, components):
        self.components = pd.concat([self.components, components])
        print(self.components)

    def gravity_center(self):
        df = self.components.copy()

        # Calculate the total weight
        total_weight = df['mass'].sum()
        
        # Compute the weighted sum for each coordinate
        x_cg = (df['x'] * df['mass']).sum() / total_weight
        y_cg = (df['y'] * df['mass']).sum() / total_weight
        z_cg = (df['z'] * df['mass']).sum() / total_weight
    
        # Return the center of gravity as a list [x, y, z]
        return np.array([x_cg, y_cg, z_cg])
    
    def totalMass(self):
        df = self.components.copy()
        return df['mass'].sum()
        

    def showBendingLoads(self):
        return

    def showBendingMoment(self):
        return

    def showShearForce(self):
        return
        