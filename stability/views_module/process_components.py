from django.http import JsonResponse
from django.shortcuts import render
import json
import pandas as pd
from ..Modules.gravityCenter import gravity_center

def process_components(request):
    data = json.loads(request.body)
    request.session['car_components'] = data

    # components = data.get('components', [])
    # # Process the components data
    # column_names = ["component_name", "mass", "x", "y", "z"]
    # df = pd.DataFrame(components, columns=column_names)
    # gravity_center_object = gravity_center(df)
    # print(gravity_center_object.gravity_center())
    
    # return render(request, 'components_form.html', {})