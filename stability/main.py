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



def main(request):
    """
    Main view function to handle different types of forms and requests from the front-end.
    The forms correspond to the action the user click, for example change the geometry
    of the suspention, change angle of the chassis, compute maximum velocity and 
    compute the rotation of the chassis when rounding a curve.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object containing metadata about the request.

    Returns
    -------
    HttpResponse
        Renders the stability page with appropriate forms, or redirects based on the request type.
    """
    # Retrieve max_rotation from the session
    max_rotation = request.session.get('max_rotation')

    if request.method == 'POST':
        # Handle requests based on specific keys in POST data
        if 'hu' in request.POST:
            return process_geometry(request)

        elif 'angle' in request.POST:
            return process_angle(request)

        elif 'radius' in request.POST:
            return curve_max_velocity(request)

        elif 'velocity' in request.POST:
            return curve_chassis_rotation(request)

        elif request.content_type == 'application/json':
            # Handle JSON payloads
            process_components(request)

    # Render the stability page with the appropriate forms
    return render(request, 'stability.html', {
        'geometry_form': SuspensionForm(),
        'angle_form': thetaForm(max_rotation=max_rotation),
        'max_rotation': max_rotation,
        'radius_form': radius_form,
        'velocity_form': velocity_form,
    })



def components_frontend(request):
    return render(request, 'components_form.html', {})