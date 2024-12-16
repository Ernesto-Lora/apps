from django.shortcuts import render
import json

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import io
import base64
import pandas as pd

from ..Modules.lines.omega import omega
from ..Modules import frontStability

from ..Modules.lines.compute_roll_center import ComputeRollCenter
from ..Modules.gravityCenter import gravity_center
from ..Modules.lines.system_object import system_object

def compute_distance(x,y):
    z = x-y
    return  np.linalg.norm(z[:2])

def process_object_and_render(request, template, context):
    """
    Processes a given object, computes roll and gravity centers, generates a plot, 
    and renders the output into a specified template with updated context.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object containing session data.
    template : str
        The name of the template to render.
    context : dict
        The context dictionary to be updated and passed to the template.

    Returns
    -------
    HttpResponse
        The rendered HTTP response with the updated context.

    Notes
    -----
    - This function assumes the presence of certain methods and attributes, such as `omega`, `ComputeRollCenter`, 
      and `gravity_center`, which are not defined within this code.
    - The `frontStability.plot_system` function is expected to handle the plotting of the object and gravity center.
    """

    max_rotation = request.session.get('max_rotation')
    object_data = request.session.get('object_data')
    angle_session = request.session.get('angle')
    roll_center = request.session.get('roll_center')
    gravity_center_val = request.session.get('gravity_center_val')

    distance = compute_distance(np.array(roll_center), np.array(gravity_center_val))
    request.session['distance'] = float(distance)
    #distance = request.session.get('distance')

    # Initialize plot
    fig, ax = plt.subplots()

    # Perform object-specific processing
    object = system_object(**object_data)
    omega(object)
    object.theta = angle_session

    # Plot system and configure plot settings
    frontStability.plot_system(object, gravity_center_val, fig, ax)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.ylim(-0.1, 0.8)
    plt.xlim(-1.2, 1.2)

    # Save plot as SVG and encode in Base64
    buffer = io.BytesIO()
    plt.savefig(buffer, bbox_inches='tight', format='svg')
    buffer.seek(0)
    svg_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    # Update context with computed values and SVG data
    context.update({
        'svg_base64': svg_base64,
        'roll_center_x': round(roll_center[0], 3),
        'roll_center_y': round(roll_center[1], 3),
        'gravity_center_x': round(gravity_center_val[0], 3),
        'gravity_center_y': round(gravity_center_val[1], 3),
        'max_rotation': round(np.rad2deg(max_rotation), 3),
        'distance': round(distance, 3)
    })
    
    table_data = request.session.get('table_data')
    context.update({
        'table_data': json.dumps(table_data)  # Pass data as JSON to the template
    }) 

    # Render and return the response
    return render(request, template, context)


