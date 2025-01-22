# How to Create an App

Here, an example app will be created.

## Step 1: Create the App Through the Project

To create a new Django app, use:

```bash
py manage.py startapp example_app
```

## Step 2: Create the Form That Will Act as the Input

Create the file `forms.py`. The form will consist of a class that contains the input variables. These variables will be sent to the server, and we will return an output. If different variables need to be sent, we need to create a new class with different variables as shown below:

```python
from django import forms

class ExampleForm(forms.Form):
    example = forms.FloatField(label='Example Variable', initial=1)

class ExampleForm2(forms.Form):
    example2 = forms.FloatField(label='Example Variable 2', initial=3)
```

## Step 3: Create the Functionality Module

Create the `modules` directory inside the `example_app` directory to code the functionalities.

Create `example_functions.py` inside `modules` and write the functionalities and classes as shown below:

```python
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class ExampleClass:
    def __init__(self, example):
        self.example = example

    def double(self):
        return self.example * 2

    def multiply(self, num):
        return self.double() * num

    def plot(self):
        x = np.linspace(0, 10)
        y = self.example * x
        plt.plot(x, y)

        # Save the plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Convert to base64 for embedding in HTML
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        plt.close()
        return image_base64
```

## Step 4: Main Logic

The main function will receive an HTTP request from the frontend (user). When the user first enters the page, we will send the HTML template (see the next section) with the forms so the user can see the inputs. When the user submits the forms, they are sending a `POST` HTTP request, meaning they are sending information (the inputs). Our server receives this and, depending on the information, returns a response with an output so the user can see it.

In the example below, we are expecting to receive two different variables from separate forms. When the first example variable is received, we create a custom object that comes from our modules. We perform some operations (methods) and then send back the response and the forms. We also save the variables in the session. The forms are sent again so the user can introduce other inputs. When the second example variable is received, as we have saved the first variable in session variables, we can use it to perform further operations.

```python
from django.shortcuts import render
from .modules.example_functions import ExampleClass
from .forms import ExampleForm, ExampleForm2

def main(request):
    if request.method == 'POST':
        if 'example' in request.POST:
            form = ExampleForm(request.POST)
            if form.is_valid():  # Validate the form first
                # Get parameters from the form
                example = form.cleaned_data['example']

                example_object = ExampleClass(example=example)
                result = example_object.double()

                request.session['example'] = example #save data ...


                return render(request, 'example.html', {
                    'form': ExampleForm(),
                    'form2': ExampleForm2(),
                    'result': round(result, 2),
                })

        if 'example2' in request.POST:
            form = ExampleForm2(request.POST)  # Ensure you're instantiating the correct form
            if form.is_valid():  # Validate the second form
                example = request.session.get('example')  # Retrieve stored session value
                example2 = form.cleaned_data['example2']

                example_object = ExampleClass(example=example)
                result = example_object.double()
                result2 = example_object.multiply(example2)

                return render(request, 'example.html', {
                    'form': ExampleForm(),
                    'form2': ExampleForm2(),
                    'result': round(result, 2),
                    'result2': round(result2, 2)
                })

    # Render initial forms if not POST
    return render(request, 'example.html', {
        'form': ExampleForm(),
        'form2': ExampleForm2()
    })
```

## Step 5: Create the HTML Template

In the template, we need to receive the form so the user can see it. We need to show the input and display the output when it is sent. The form has a `POST` method, meaning the information will be sent. As we are sending separate variables to perform different operations, we need to specify that two forms will be received. Create the `example.html` file in the `templates` directory and write the components as shown below:

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Example</title>
    <!-- <link rel="stylesheet" href="{% static 'css/styles.css' %}"> -->
  </head>
  <body>
    <div id="container">
      <h1>Example App</h1>

      <form method="post">
        {% csrf_token %} {{ form.as_p }}
        <button type="submit">Double</button>
      </form>

      <form method="post">
        {% csrf_token %} {{ form2.as_p }}
        <button type="submit">Multiply the Result</button>
      </form>

      {% if result %}
      <p>The double of the example variable is: {{ result }}</p>
      {% endif %} {% if result2 %}
      <p>
        When multiplied by the second example variable, the result is: {{
        result2 }}
      </p>
      {% endif %}
    </div>
  </body>
</html>
```

## Step 6: Add the App to a Route (URL) on the Server

Add the route for the new app in the project's `urls.py` file:

```python
from django.contrib import admin
from django.urls import path
from example_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('example/', views.main, name='example')  # The new URL
]
```
