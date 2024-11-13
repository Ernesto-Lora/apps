# Create your views here.
from django.shortcuts import render

# Create your views here.
import matplotlib.pyplot as plt

from .Modules import frontStability, gravityCenter, rollover, chassis_stiffnes
import io
import base64
import pandas as pd
from .forms import SuspensionForm

def app(request):
    if request.method == 'POST':
        print(f'hola')
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

            # Generate the scientific image
            suspension = frontStability.suspentionChasisSystem(
                D=D, Dtw=Dtw, ht=ht, hu=hu, hb=hb, lu=lu, lb=lb,
                philu=philu, philb=philb, phiru=phiru, phirb=phirb
            )

            load = gravityCenter.loads(components=pd.read_excel("stability/components.xlsx"))
            roll_center = suspension.getRollCenter()
            gravity_center = load.centreGravity()

            suspension.addChassisAngle(theta=theta)
            suspension.addCenterGravity(cog=gravity_center)
            image_base64 = suspension.showAll()

            chassis_stiffnes_i = chassis_stiffnes.chassis_stiffness(D = D, kw=22000)
            roll_over = rollover.rollover(load, suspension, chassis_stiffnes_i)

            max1 = roll_over.max_speed_weigth(R=400)
            max2 = roll_over.max_speed_angle(R=400)


            return render(request, 'stability.html', {'form': form, 
                                                      'image_base64': image_base64,
                                                      'roll_center_x': roll_center[0],
                                                      'roll_center_y': round(roll_center[1],3),
                                                      'gravity_center_x': round(gravity_center[0], 3),
                                                      'gravity_center_y': round(gravity_center[1], 3),
                                                      'max1': round(max1 ,3),
                                                      'max2': round(max2 ,3)
                                                      })
    else:
        form = SuspensionForm()

    return render(request, 'stability.html', {'form': form})
