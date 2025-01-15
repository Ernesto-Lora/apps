from django.shortcuts import render

from .modules.example_functions import example_class

import io
import base64
import pandas as pd
from example_app.forms import example_Form


def main(request):
    if request.method == 'POST':
        form = example_Form(request.POST)
        if form.is_valid():
            # Get parameters from the form
            example = form.cleaned_data['example']

            example_object = example_class(example=example)
            
            image_base64 = example_object.plot()

            result = example_object.result()

            return render(request, 'example.html', {
                                    'form': form,
                                    'result': round(result, 2),
                                    'image_base64': image_base64,
                                })
    else:
        form = example_Form()

    return render(request, 'example.html', {'form': form})