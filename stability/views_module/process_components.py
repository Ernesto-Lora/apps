from django.http import JsonResponse
from django.shortcuts import render
import json
import pandas as pd
from ..Modules.gravityCenter import gravity_center
import numpy as np

from ..forms import SuspensionForm, thetaForm, radius_form, velocity_form
from ..views_module.process_object_and_render import process_object_and_render

def compute_distance(x,y):
    z = x-y
    return  np.linalg.norm(z[:2])

def process_components(request):
    data = request.POST.get('components', '{}') #Data send from front-end
    components = json.loads(data)  # Parse the JSON string
    column_names = ["component_name", "mass", "x", "y", "z"]
    df = pd.DataFrame(components, columns=column_names)

    # Compute gravity center and distance
    gravity_center_object = gravity_center(df)
    gravity_center_val = gravity_center_object.gravity_center()
    print(gravity_center_val)
    request.session['gravity_center_val'] = gravity_center_val.tolist()
    request.session['total_mass'] = float(gravity_center_object.totalMass())
    request.session['table_data'] = components  # Save to session

    return process_object_and_render(request,
                                        'stability.html',
                                        {'geometry_form': SuspensionForm(),
                                        'angle_form': thetaForm(max_rotation=request.session.get('max_rotation')),
                                        'radius_form': radius_form,
                                        'velocity_form': velocity_form})