from matplotlib.patches import Circle

def show_circle(point, color, fig, ax):
    '''point: np.array([x,y,z])'''
    # Add circle to the plot
    circle = Circle((point[0], point[1]), 0.025, fill =True, color = color)
    ax.add_patch(circle)