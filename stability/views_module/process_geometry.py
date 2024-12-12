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
from ..forms import SuspensionForm, thetaForm, radius_form, velocity_form

from ..Modules.lines.system_object import system_object
from ..Modules.lines.max_rotation import maxRotation
from ..Modules.lines.compute_roll_center import ComputeRollCenter

from .process_object_and_render import process_object_and_render

def process_geometry(request):
    geometry_form = SuspensionForm(request.POST)
    if geometry_form.is_valid():
        # Extract and validate geometry_form data...
        D = geometry_form.cleaned_data['D']
        Dtw = geometry_form.cleaned_data['Dtw']
        ht = geometry_form.cleaned_data['ht']
        hu = geometry_form.cleaned_data['hu']
        hb = geometry_form.cleaned_data['hb']
        lu = geometry_form.cleaned_data['lu']
        lb = geometry_form.cleaned_data['lb']
        philu = geometry_form.cleaned_data['philu']
        philb = geometry_form.cleaned_data['philb']
        phiru = geometry_form.cleaned_data['phiru']
        phirb = geometry_form.cleaned_data['phirb']

        warnings = []
        if hu <= hb:
            warnings.append("The Upper Wishbone point (hu) must be above the lower Wishbone point (hb).")
        # Handle warnings
        if warnings:
            return render(request, 'stability.html', {'geometry_form': geometry_form, 'warnings': warnings})
        
        # Create object and calculate max_rotation
        object = system_object(
        D=D, Dtw=Dtw, ht=ht, hu=hu, hb=hb, lu=lu, lb=lb,
        philu=philu, philb=philb, phiru=phiru, phirb=phirb)

        max_rotation = maxRotation(object)
        roll_center = ComputeRollCenter(object)

        request.session['roll_center_0'] = roll_center.tolist()
        request.session['max_rotation'] = max_rotation
        request.session['object_data'] = geometry_form.cleaned_data  # Save essential data
        request.session.save()
        
        # Plot and render
        return  process_object_and_render(request, object, max_rotation,
            'stability.html',
                {'geometry_form': geometry_form,
            'angle_form': thetaForm(max_rotation=max_rotation),
            'radius_form': radius_form,
            'velocity_form': velocity_form})
    
