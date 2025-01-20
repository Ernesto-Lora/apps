from django.shortcuts import render

from .modules.example_functions import example_class

import io
import base64
import pandas as pd
from example_app.forms import example_Form, example_Form_2


def main(request):
    if request.method == 'POST':
        if 'example' in request.POST:
            form = example_Form(request.POST)
            if form.is_valid():  # Validate the form first
                # Get parameters from the form
                example = form.cleaned_data['example']

                example_object = example_class(example=example)
                result = example_object.double()
                request.session['example'] = example

                return render(request, 'example.html', {
                    'form': example_Form(),
                    'form2': example_Form_2(),
                    'result': round(result, 2),
                })
        
        if 'example2' in request.POST:
            form = example_Form_2(request.POST)  # Ensure you're instantiating the correct form
            if form.is_valid():  # Validate the second form
                example = request.session.get('example')  # Retrieve stored session value
                example2 = form.cleaned_data['example2']

                example_object = example_class(example=example)
                result = example_object.double()
                result2 = example_object.multiply(example2)

                return render(request, 'example.html', {
                    'form': example_Form(),
                    'form2': example_Form_2(),
                    'result': round(result, 2),
                    'result2': round(result2, 2)
                })

    # Render initial forms if not POST
    return render(request, 'example.html', {
        'form': example_Form(),
        'form2': example_Form_2()
    })
