from django.http import JsonResponse
import json
import pandas as pd
from ..Modules.gravityCenter import gravity_center
def process_components(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        components = data.get('components', [])
        # Process the components data
        column_names = ["component_name", "mass", "x", "y", "z"]
        df = pd.DataFrame(components, columns=column_names)
        gravity_center_object = gravity_center(df)
        print(gravity_center_object.gravity_center())
        
        return JsonResponse({'status': 'success', 'message': 'Components processed'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)