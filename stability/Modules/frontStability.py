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