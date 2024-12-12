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
    max_rotation = request.session.get('max_rotation')
    object_data = request.session.get('object_data') 
    angle_form = thetaForm(max_rotation=max_rotation, data=request.POST)
    if angle_form.is_valid() and object_data:
        # Recreate object and process
        object = system_object(**object_data)

        object.theta = np.deg2rad(angle_form.cleaned_data['angle'])
        request.session['angle'] = np.deg2rad(angle_form.cleaned_data['angle'])   

        return process_object_and_render(request, object, max_rotation ,
                'stability.html',
            {'geometry_form': SuspensionForm(),
            'angle_form': angle_form,
            'radius_form': radius_form,
            'velocity_form': velocity_form,
            })