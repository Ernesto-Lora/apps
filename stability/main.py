# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import io
import base64
import pandas as pd
from .forms import SuspensionForm, thetaForm, radius_form, velocity_form

from .Modules.lines.system_object import system_object
from .Modules.lines.omega import omega
from .Modules.lines.max_rotation import maxRotation
from .Modules import frontStability

from .Modules.lines.compute_roll_center import ComputeRollCenter
from .Modules.gravityCenter import gravity_center
from .Modules.chassis_stiffnes import chassis_stiffness
from .Modules.rollover import rollover

from .views_module.process_object_and_render import process_object_and_render
from .views_module.process_geometry import process_geometry
from .views_module.process_angle import process_angle
from .views_module.curve_max_velocity import curve_max_velocity
from .views_module.curve_chassis_rotation import curve_chassis_rotation
from .views_module.process_components import process_components



import json
import pandas as pd

def main(request):
    """
    Main view function to handle different types of forms and requests from the front-end.
    """
    # Retrieve max_rotation from the session
    max_rotation = request.session.get('max_rotation')
    
    # Initialize session values if they do not exist
    if request.session.get('angle') is None:
        request.session['angle'] = 0
    
    if request.session.get('table_data') is None:
        request.session['table_data'] = [
            ['Front bumper', 13, 0, 0.3, 0],
            ['Radiator', 60, 0, 0.4, 0.3],
            ['engine/trans', 85, 0.5, 0.4, 1.1],
            ['Fuel tanks + luggage', 65, 0.5, 0.45, 3.3],
            ['Luggage', 50, 0, 0.5, 3.85],
            ['Rear Bumper', 14, 0, 0.3, 4.2],
            ['Front Left Corner', 90, -0.7, 0.3, 0],
            ['Front Right Corner', 90, 0.7, 0.3, 0],
            ['Rear Left Corner', 125, -0.7, 0.3, 4],
            ['Rear Right Corner', 125, 0.7, 0.3, 4],
            ['Caja sonido', 2, 0.3, 0.4, 4],
        ]
    
    if request.session.get('gravity_center_val') is None:
        components = request.session['table_data']
        column_names = ["component_name", "mass", "x", "y", "z"]
        df = pd.DataFrame(components, columns=column_names)
        gravity_center_object = gravity_center(df)
        request.session['gravity_center_val'] = gravity_center_object.gravity_center().tolist()
        request.session['total_mass'] = float(gravity_center_object.totalMass())
    
    if request.method == 'POST':
        # Handle different POST requests
        if 'hu' in request.POST:
            return process_geometry(request)
        elif 'angle' in request.POST:
            return process_angle(request)
        elif 'radius' in request.POST:
            return curve_max_velocity(request)
        elif 'velocity' in request.POST:
            return curve_chassis_rotation(request)
        elif request.content_type == 'application/json':
            return process_components(request)
    
    # Pass serialized table_data to the template
    return render(request, 'stability.html', {
        'geometry_form': SuspensionForm(),
        'angle_form': thetaForm(max_rotation=max_rotation),
        'max_rotation': max_rotation,
        'radius_form': radius_form,
        'velocity_form': velocity_form,
        'table_data': json.dumps(request.session['table_data']),  # Serialize to JSON
    })




def components_frontend(request):
    return render(request, 'components_form.html', {})