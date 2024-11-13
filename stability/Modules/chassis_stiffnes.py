import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class chassis_stiffness():
    def __init__(self, D, kw):
        self.D = D
        self.kw = kw

    def chassis_stiffness(self):
        """
        Return chassis stiffness in Nm/radians
        """
        D = self.D
        kw = self.kw
        return D**2*kw

        