# Create your views here.
from django.shortcuts import render

# Create your views here.
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

def compute_distance(x,y):
    z = x-y
    return  np.linalg.norm(z[:2])

def process_object_and_render(request, object, max_rotation, template, context):
    fig, ax = plt.subplots()
    omega(object)
    roll_center = ComputeRollCenter(object)
    gravity_center_object = gravity_center(pd.read_excel("static/stability/components.xlsx"))
    gravity_center_val = gravity_center_object.gravity_center()
    distance = compute_distance(roll_center, gravity_center_val)
    frontStability.plot_system(object, fig, ax)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.ylim(-0.1, 0.8)
    plt.xlim(-1.2, 1.2)

    buffer = io.BytesIO()
    plt.savefig(buffer, bbox_inches='tight', format='svg')
    buffer.seek(0)
    svg_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    print(round(roll_center[1], 3))
    print(request.session['max_rotation'])

    context.update({
        'svg_base64': svg_base64,
        'roll_center_x': round(roll_center[0], 3),
        'roll_center_y': round(roll_center[1], 3),
        'gravity_center_x': round(gravity_center_val[0], 3),
        'gravity_center_y': round(gravity_center_val[1], 3),
        'max_rotation': round(np.rad2deg(max_rotation), 3),
        'distance': round(distance, 3)
    })
    return render(request, template, context)