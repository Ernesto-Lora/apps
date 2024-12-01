# Create your views here.
from django.shortcuts import render

# Create your views here.
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import pandas as pd
from .forms import SuspensionForm, thetaForm

from .Modules.lines.system_object import system_object
from .Modules.lines.omega import omega
from .Modules.lines.max_rotation import maxRotation
from .Modules import frontStability

from .Modules.lines.compute_roll_center import ComputeRollCenter
from .Modules.gravityCenter import gravity_center


def app(request):
    if request.method == 'POST':
        form = SuspensionForm(request.POST)
        if form.is_valid():
            # Get parameters from the form
            D = form.cleaned_data['D']
            Dtw = form.cleaned_data['Dtw']
            ht = form.cleaned_data['ht']
            hu = form.cleaned_data['hu']
            hb = form.cleaned_data['hb']
            lu = form.cleaned_data['lu']
            lb = form.cleaned_data['lb']
            philu = form.cleaned_data['philu']
            philb = form.cleaned_data['philb']
            phiru = form.cleaned_data['phiru']
            phirb = form.cleaned_data['phirb']

            theta = form.cleaned_data['theta']

            # Validate conditions
            warnings = []
            if hu <= hb:
                warnings.append("The Upper Wishbone point (hu) must be above the lower Wishbone point (hb).")
            if not (ht > hu and ht > hb):
                warnings.append("The Tire radius (ht) must be larger than the upper (hu) and lower (hb) wishbone points.")
            
            if warnings:
                # Render the template with the warnings but no plot
                return render(request, 'stability.html', {'form': form, 'warnings': warnings[0]})
            
            object = system_object(
                D=D, Dtw=Dtw, ht=ht, hu=hu, hb=hb, lu=lu, lb=lb,
                philu=philu, philb=philb, phiru=phiru, phirb=phirb,
                theta = theta
            )
            max_rotation = maxRotation(object)

            if theta >= np.degrees(max_rotation):
                warnings.append("The rotation angle θ cannot exceed the Maximum Rotation Angle.")

            if warnings:
                # Render the template with the warnings but no plot
                return render(request, 'stability.html', {'form': form, 'warnings': warnings[0]})

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
            
            # Convert to base64 for embedding in HTML
            svg_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            buffer.close()

            #chassis_stiffnes_i = chassis_stiffnes.chassis_stiffness(D = D, kw=22000)
            #roll_over = rollover.rollover(load, suspension, chassis_stiffnes_i)

            #max1 = roll_over.max_speed_weigth(R=400)
            #max2 = roll_over.max_speed_angle(R=400)
            max1 = 10
            max2 = 10

            return render(request, 'stability.html', {'form': form, 
                                                      'svg_base64': svg_base64,
                                                      'roll_center_x': round(roll_center[0],3),
                                                      'roll_center_y': round(roll_center[1],3),
                                                      'gravity_center_x': round(gravity_center_val[0],3),
                                                      'gravity_center_y': round(gravity_center_val[1],3),
                                                      'max_rotation': round(np.degrees(max_rotation), 3),
                                                      'max1': round(max1 ,3),
                                                      'max2': round(max2 ,3)
                                                      })
    else:
        form = SuspensionForm()

    return render(request, 'stability.html', {'form': form})



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
    print("hola")
    return render(request, template, context)


def app2(request):
    max_rotation = request.session.get('max_rotation')  # Retrieve max_rotation
    object_data = request.session.get('object_data')  # Get stored object data
    print(request.POST)
    if request.method == 'POST':
        if 'hu' in request.POST:
            print("Geometry form send")
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
                request.session['max_rotation'] = max_rotation
                request.session['object_data'] = geometry_form.cleaned_data  # Save essential data
                
                # Plot and render
                return process_object_and_render(request, object, max_rotation,
                    'stability.html',
                      {'geometry_form': geometry_form,
                    'angle_form': thetaForm(max_rotation=max_rotation),})
            
        elif 'angle' in request.POST:
            print("angle form has been send")
            print(max_rotation)
            angle_form = thetaForm(max_rotation=max_rotation, data=request.POST)
            if angle_form.is_valid() and object_data:
                # Recreate object and process
                object = system_object(**object_data)

                object.theta = np.deg2rad(angle_form.cleaned_data['angle'])

                return process_object_and_render(request, object, max_rotation ,
                        'stability.html',
                    {'geometry_form': SuspensionForm(),
                    'angle_form': angle_form,})
            
    print("nothing is happening")
    return render(request, 'stability.html', {
        'geometry_form': SuspensionForm(),
        'angle_form': thetaForm(max_rotation=max_rotation),
        'max_rotation': max_rotation,
    })
