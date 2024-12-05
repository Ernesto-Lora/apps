import matplotlib.pyplot as plt
import numpy as np

def show_line(v1, v2, fig, ax):
    ax.plot([v1[0], v2[0]], [v1[1], v2[1]], color="black")
