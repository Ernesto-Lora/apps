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



def app2(request):
    max_rotation = request.session.get('max_rotation')  # Retrieve max_rotation
    object_data = request.session.get('object_data')  # Get stored object data
    angle_session = request.session.get('angle')
    roll_center = request.session.get('roll_center_0')
    
    if request.method == 'POST':
        if 'hu' in request.POST:
            return process_geometry(request)
            
            
        elif 'angle' in request.POST:
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
            
        elif 'radius' in request.POST:
            radius_form_data = radius_form(request.POST)
            
            if radius_form_data.is_valid() and object_data:
                # Recreate object and process
                radius = radius_form_data.cleaned_data['radius']
                distance = radius_form_data.cleaned_data['distance']
                object = system_object(**object_data)
                object.theta = angle_session

                gravity_center_object = gravity_center(pd.read_excel("static/stability/components.xlsx"))

                chassis_stiffnes_i = chassis_stiffness(D = object.D, kw=12000)
                #roll_center = ComputeRollCenter(object)
                #roll_center = np.array([0,0,0])

                roll_over = rollover(gravity_center_object,
                                      np.array(roll_center), max_rotation, object.D,
                                     chassis_stiffnes_i)
                print(radius)
                max1 = roll_over.max_speed_weigth_modified(R=radius, distance=distance)
                #max2 = roll_over.max_speed_angle(R=radius)

                return process_object_and_render(request, object, max_rotation ,
                        'stability.html',
                    {'geometry_form': SuspensionForm(),
                    'angle_form': thetaForm(max_rotation=max_rotation),
                    'radius_form': radius_form,
                    'velocity_form': velocity_form,
                    'max_speed_weigth_modified': round(max1*3.6),
                    'radius': radius})
            
        elif 'velocity' in request.POST:
            velocity_form_data = velocity_form(request.POST)
            
            if velocity_form_data.is_valid() and object_data:
                # Recreate object and process
                velocity = velocity_form_data.cleaned_data['velocity']
                k = velocity_form_data.cleaned_data['k']
                radius = velocity_form_data.cleaned_data['radius_for_rotation']
                distance = velocity_form_data.cleaned_data['distance']
                
                object = system_object(**object_data)
                object.theta = angle_session

                gravity_center_object = gravity_center(pd.read_excel("static/stability/components.xlsx"))
                chassis_stiffnes_i = chassis_stiffness(D = object.D, kw=k)
                #roll_center = ComputeRollCenter(object)
                #roll_center = np.array([0,0,0])

                roll_over = rollover(gravity_center_object,
                                      np.array(roll_center), max_rotation, object.D,
                                     chassis_stiffnes_i)
                
                rotation_curve = roll_over.rotation_curve(R = radius, v=velocity, distance=distance)
                max1 = roll_over.max_speed_weigth_modified(R= radius)

                return process_object_and_render(request, object, max_rotation ,
                        'stability.html',
                    {'geometry_form': SuspensionForm(),
                    'angle_form': thetaForm(max_rotation=max_rotation),
                    'radius_form': radius_form,
                    'velocity_form': velocity_form,
                    'max_speed_weigth_modified': round(max1*3.6),
                    'rotation_curve': round(np.rad2deg(rotation_curve),3),
                    'velocity': velocity,
                    'k': k,
                    'radius': radius},
                    )
            
    return render(request, 'stability.html', {
        'geometry_form': SuspensionForm(),
        'angle_form': thetaForm(max_rotation=max_rotation),
        'max_rotation': max_rotation, 
        'radius_form': radius_form,
        'velocity_form': velocity_form,
    })


def components_frontend(request):
    return render(request, 'components_form.html', {})