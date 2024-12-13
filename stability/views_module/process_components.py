from django.http import JsonResponse
from django.shortcuts import render
import json
import pandas as pd
from ..Modules.gravityCenter import gravity_center
import numpy as np

def compute_distance(x,y):
    z = x-y
    return  np.linalg.norm(z[:2])

def process_components(request):
    roll_center = np.array(request.session.get('roll_center'))
    data = json.loads(request.body) #Data send from front-end
    components = data.get('components', [])
    column_names = ["component_name", "mass", "x", "y", "z"]
    df = pd.DataFrame(components, columns=column_names)

    # Compute gravity center and distance
    gravity_center_object = gravity_center(df)
    gravity_center_val = gravity_center_object.gravity_center()
    distance = compute_distance(roll_center, gravity_center_val)
    
    request.session['distance'] = float(distance)
    request.session['gravity_center_val'] = gravity_center_val.tolist()
    request.session['total_mass'] = float(gravity_center_object.totalMass())
    request.session['table_data'] = data['components']  # Save to session