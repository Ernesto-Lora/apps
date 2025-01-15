# How to create an app

Here an example app will be created

# step 1. Create the app trough the project

To create a new Django app, use:

```bash
py manage.py startapp example_app
```

# step 2. Create the Form that will act as the input.

Create the file forms.py and inside it create a class as bellow:

```python
from django import forms

class example_Form(forms.Form):
    example = forms.FloatField(label='Example Variable', initial=1)
```

# step 3. Create the functionality module.

If the functionalities are simple and short to write, the file models.py will be sufficient. If the functionalities need to be modularized or extend, create the modules dictionary inside the example_app dictionary.

-- Create example_functions.py inside modules and write the functionalites and classes as bellow:

```python
import numpy as np
import matplotlib.pyplot as plt
import io
import base64


class example_class:
    def __init__(self, example):
        self.example = example

    def multiply(self):
        self.example *= 2

    def plot(self):
        self.multiply()
        x = np.linspace(0,10)
        y = self.example*x
        plt.plot(x,y)
        plt.show()
        # Save the plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Convert to base64 for embedding in HTML
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        return image_base64

```

# step 4. Create the HTML template

We need to show the input and show the output when this is send it. Create the example.html file in the templates directory and write the components as bellow:

```HTML
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>example</title>
    <!-- <link rel="stylesheet" href="{% static 'css/styles.css' %}"> -->

</head>
<body>

    <!-- Input -->
    <div id="container">
        <h1>Spring UTS Analysis</h1>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Generate Analysis</button>
        </form>

        <!-- Output -->
        {% if result %}
        <p>The slope is: {{result}}</p>
        {% endif %}

        {% if image_base64 %}
        <div class="image-container">
            <h3>Slop plot.</h3>
            <img src="data:image/png;base64,{{ image_base64 }}" alt="example Image">
        </div>
        {% endif %}
    </div>
</body>
</html>
```

# step 5. Main logic.

Create the main.py inside the app directory. Write the logic as bellow

```python
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
```

# step 6. Add the app to the an route (url) on the server.

```python
from django.contrib import admin
from django.urls import path
import stability
import springUTS.main
import stability.main
import example_app.main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stability/', stability.main.main, name = 'stability'),
    path('springUTS/', springUTS.main.main, name = 'springUTS'),
    path('example/', example_app.main.main, name = 'example' ) # the new url
]

```
