import numpy as np

from matplotlib.patches import Arc

def show_chassis_angle(object, fig, ax):
    # Define parameters for the angle and limits
    theta = object.theta  # angle in radians 
    line_length = 0.5  # Line as horizontal reference in the chassis

    # Add the red dashed line indicating the angle θ
    x_end = line_length * np.cos(theta)
    y_end = object.ycc + line_length * np.sin(theta)
    ax.plot([0, x_end], [object.ycc, y_end],
             'r--', label=r'$\theta$')  # Red dashed line for angle

    # Add a horizontal reference line (optional based on your image)
    ax.plot([-0.3*object.D, 0.3*object.D],
             [object.ycc, object.ycc], color='red', linewidth=1)

    # Arc representing the angle θ
    arc_radius = 0.2  
    angle_start = 0  
    angle_end = np.degrees(theta)  
    arc = Arc((0, object.ycc),  # Center of the arc
              width=2*arc_radius, height=2*arc_radius,  # Dimensions of the arc
              theta1=angle_start, theta2=angle_end,  
              color='r', linestyle = "dashed",linewidth=1.5)

    ax.add_patch(arc)
