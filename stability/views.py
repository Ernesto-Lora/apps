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


def process_object_and_render(request, object, max_rotation,template, context):
    fig, ax = plt.subplots()
    omega(object)
    roll_center = ComputeRollCenter(object)
    gravity_center_object = gravity_center(pd.read_excel("static/stability/components.xlsx"))
    gravity_center_val = gravity_center_object.gravity_center()
    frontStability.plot_system(object, fig, ax)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.ylim(-0.1, 0.8)
    plt.xlim(-1.2, 1.2)

    buffer = io.BytesIO()
    plt.savefig(buffer, bbox_inches='tight', format='svg')
    buffer.seek(0)
    svg_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    context.update({
        'svg_base64': svg_base64,
        'roll_center_x': round(roll_center[0], 3),
        'roll_center_y': round(roll_center[1], 3),
        'gravity_center_x': round(gravity_center_val[0], 3),
        'gravity_center_y': round(gravity_center_val[1], 3),
        'max_rotation': round(np.rad2deg(max_rotation), 3)
    })
    return render(request, template, context)


def app2(request):
    max_rotation = request.session.get('max_rotation')  # Retrieve max_rotation
    object_data = request.session.get('object_data')  # Get stored object data
    angle_session = request.session.get('angle')
    roll_center = request.session.get('roll_center_0')
    
    if request.method == 'POST':
        if 'hu' in request.POST:
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
                
                # Plot and render
                return process_object_and_render(request, object, max_rotation,
                    'stability.html',
                      {'geometry_form': geometry_form,
                    'angle_form': thetaForm(max_rotation=max_rotation),
                    'radius_form': radius_form,
                    'velocity_form': velocity_form})
            
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
                max1 = roll_over.max_speed_weigth_modified(R=radius)
                max2 = roll_over.max_speed_angle(R=radius)

                return process_object_and_render(request, object, max_rotation ,
                        'stability.html',
                    {'geometry_form': SuspensionForm(),
                    'angle_form': thetaForm(max_rotation=max_rotation),
                    'radius_form': radius_form,
                    'velocity_form': velocity_form,
                    'max_speed_weigth_modified': round(max1*3.6),
                    'max_speed_angle': round(max2*3.6)})
            
        elif 'velocity' in request.POST:
            velocity_form_data = velocity_form(request.POST)
            
            if velocity_form_data.is_valid() and object_data:
                # Recreate object and process
                velocity = velocity_form_data.cleaned_data['velocity']
                k = velocity_form_data.cleaned_data['k']
                radius = velocity_form_data.cleaned_data['radius_for_rotation']
                object = system_object(**object_data)
                object.theta = angle_session

                gravity_center_object = gravity_center(pd.read_excel("static/stability/components.xlsx"))

                chassis_stiffnes_i = chassis_stiffness(D = object.D, kw=k)
                #roll_center = ComputeRollCenter(object)
                #roll_center = np.array([0,0,0])

                roll_over = rollover(gravity_center_object,
                                      np.array(roll_center), max_rotation, object.D,
                                     chassis_stiffnes_i)
                rotation_curve = roll_over.rotation_curve(R = radius, v=velocity)
                max1 = roll_over.max_speed_weigth_modified(R= radius)
                max2 = roll_over.max_speed_angle(R= radius)

                return process_object_and_render(request, object, max_rotation ,
                        'stability.html',
                    {'geometry_form': SuspensionForm(),
                    'angle_form': thetaForm(max_rotation=max_rotation),
                    'radius_form': radius_form,
                    'velocity_form': velocity_form,
                    'max_speed_weigth_modified': round(max1*3.6),
                    'max_speed_angle': round(max2*3.6),
                    'rotation_curve': round(np.rad2deg(rotation_curve),3)},
                    )
            
    return render(request, 'stability.html', {
        'geometry_form': SuspensionForm(),
        'angle_form': thetaForm(max_rotation=max_rotation),
        'max_rotation': max_rotation, 
        'radius_form': radius_form,
        'velocity_form': velocity_form,
    })

from django.http import JsonResponse
import json
import pandas as pd

def process_components(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        components = data.get('components', [])
        # Process the components data here
        # Create a list of column names (headers)
        column_names = ["component_name", "mass", "x", "y", "z"]
        df = pd.DataFrame(components, columns=column_names)
        print(df["mass"])
        
        return JsonResponse({'status': 'success', 'message': 'Components processed'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def components_frontend(request):
    return render(request, 'components_form.html', {})