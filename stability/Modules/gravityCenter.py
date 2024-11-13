import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class loads:
    def __init__(self, components = pd.DataFrame()):
        self.components = components

    def addComponents(self, components):
        self.components = pd.concat([self.components, components])
        print(self.components)

    def centreGravity(self):
        """
        Compute the center of gravity from a dataframe with component positions and weights.
    
        Parameters:
        df (pd.DataFrame): DataFrame with columns ['Name', 'zpos (mm)', 'ypos(mm)', 'xpos(mm)', 'weight(N)']
    
        Returns:
        list: Center of gravity in the form [x, y, z]
        """
        df = self.components.copy()
        
        # Ensure the DataFrame has the required columns
        required_columns = ['Name', 'zpos(m)', 'ypos(m)', 'xpos(m)', 'weight(kg)']
        
        #print(df.columns)
        #if not all(column in df.columns for column in required_columns):
        #    raise ValueError(f"DataFrame must contain the following columns: {required_columns}")
    
        # Calculate the total weight
        total_weight = df['weight(kg)'].sum()
        
        # Compute the weighted sum for each coordinate
        x_cg = (df['xpos(m)'] * df['weight(kg)']).sum() / total_weight
        y_cg = (df['ypos(m)'] * df['weight(kg)']).sum() / total_weight
        z_cg = (df['zpos(m)'] * df['weight(kg)']).sum() / total_weight
    
        # Return the center of gravity as a list [x, y, z]
        return np.array([x_cg, y_cg, z_cg])
    
    def totalMass(self):
        df = self.components.copy()
        return df['weight(kg)'].sum()
        

    def showBendingLoads(self):
        return

    def showBendingMoment(self):
        return

    def showShearForce(self):
        return
        