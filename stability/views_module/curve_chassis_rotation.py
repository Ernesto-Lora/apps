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
from ..forms import SuspensionForm, thetaForm, radius_form, velocity_form

from ..Modules.lines.system_object import system_object
from ..Modules.lines.omega import omega
from ..Modules.lines.max_rotation import maxRotation
from ..Modules import frontStability

from ..Modules.lines.compute_roll_center import ComputeRollCenter
from ..Modules.gravityCenter import gravity_center
from ..Modules.chassis_stiffnes import chassis_stiffness
from ..Modules.rollover import rollover

from ..views_module.process_object_and_render import process_object_and_render
from ..views_module.process_geometry import process_geometry
from ..views_module.process_angle import process_angle

def curve_chassis_rotation(request):
    """
    Process the velocity form submitted
    from the front-end and compute chassis rotation based on the inputs.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object containing metadata about the request and POST data.

    Returns
    -------
    HttpResponse
        Renders the stability page with updated chassis rotation and velocity calculations.
    """
    velocity_form_data = velocity_form(request.POST)

    if velocity_form_data.is_valid():
        # Retrieve session data
        max_rotation = request.session.get('max_rotation')
        D = request.session.get('D')
        roll_center = request.session.get('roll_center')
        gravity_center_val = request.session.get('gravity_center_val')
        distance = request.session.get('distance')
        total_mass = request.session.get('total_mass')

        # Form data
        velocity = velocity_form_data.cleaned_data['velocity']
        k = velocity_form_data.cleaned_data['k']
        radius = velocity_form_data.cleaned_data['radius_for_rotation']
        distance = velocity_form_data.cleaned_data['distance']

        chassis_stiffnes_i = chassis_stiffness(D=D, kw=k)
        print(f'the total mass is: {total_mass}')
        roll_over = rollover(gravity_center_val,total_mass,
                             roll_center,distance, max_rotation, D, chassis_stiffnes_i)       

        rotation_curve = roll_over.rotation_curve(R=radius, v=velocity, distance=distance)
        max1 = roll_over.max_speed_weigth_modified(R=radius)

        return process_object_and_render(request,
                                         'stability.html',
                                         {'geometry_form': SuspensionForm(),
                                          'angle_form': thetaForm(max_rotation=max_rotation),
                                          'radius_form': radius_form,
                                          'velocity_form': velocity_form,
                                          'max_speed_weigth_modified': round(max1 * 3.6),
                                          'rotation_curve': round(np.rad2deg(rotation_curve), 3),
                                          'velocity': velocity,
                                          'k': k,
                                          'radius': radius})
