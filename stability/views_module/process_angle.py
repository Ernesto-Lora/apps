# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
from ..forms import SuspensionForm, thetaForm, radius_form, velocity_form

from ..Modules.lines.system_object import system_object
from ..views_module.process_object_and_render import process_object_and_render

def process_angle(request):
    """
    Process the angle form submitted from the front-end
      and update the session with the computed angle.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object containing metadata about the request and POST data.

    Returns
    -------
    HttpResponse
        Renders the stability page with updated angle and related calculations.
    """
    max_rotation = request.session.get('max_rotation')
    angle_form = thetaForm(max_rotation=max_rotation, data=request.POST)
    if angle_form.is_valid():
        # Recreate object and process
        request.session['angle'] = np.deg2rad(angle_form.cleaned_data['angle'])

        return process_object_and_render(request,
                                         'stability.html',
                                         {'geometry_form': SuspensionForm(),
                                          'angle_form': angle_form,
                                          'radius_form': radius_form,
                                          'velocity_form': velocity_form})
