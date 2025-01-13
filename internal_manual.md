## How It Works

The app is built using Django for the backend. The frontend interacts with the backend through forms, which are used as input for the users.

### Workflow

1. A user fills out a form and clicks a button (or presses Enter).
2. The form is sent to the Django server for processing.
3. The server processes the input using custom Python modules (the physics-based logic).
4. The server sends back a response, rendering an HTML page with the results (frontend).

---

## Project Structure

The project folder is named **`apps`**.

### Note on Django Projects

A Django project can be created using:

```bash
django-admin startproject project_name
```

By default, Django creates:

- `manage.py` file
- A module with the same name as the project (e.g., `apps`)

The `urls.py` file inside this module is where application routes are defined.

Below is an example configuration:

### URL Configuration Example

```python
from django.contrib import admin
from django.urls import path
import stability
import springUTS.main
import stability.main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stability/', stability.main.main, name='stability'),
    path('springUTS/', springUTS.main.main, name='springUTS'),
]
```

The main logic of an app is contained in the `main.py` file and in the `main` function. Here, this logic is called and assigned to a route (URL).

---

## Applications

### Note on Django Apps

To create a new Django app, use:

```bash
py manage.py startapp app_name
```

Inside each app, a manually created module named **`Modules`** contains custom functions. Django's default `views.py` file has been renamed to `main.py` in this project, as it holds the primary logic for the app.

---

### Steps to Add a Button

The `springUTS` app will be used as an example due to its simplicity.

1. **Define the input as Forms:**
   - The app's `forms.py` file specifies the inputs required from the user.

Below is the form used for the application. If a new input variable is to be added, just write it down in the form class.

```python
from django import forms

class springUTS_Form(forms.Form):
    springDiameter = forms.FloatField(label='Spring Diameter (mm)', initial=11.2)
    wireDiameter = forms.FloatField(label='Wire Diameter (mm)', initial=0.8)
    activeCoils = forms.IntegerField(label='Active Coils', initial=20)
    length = forms.FloatField(label='Length (mm)', initial=40)
    UTS = forms.FloatField(label='UTS (MPa)', initial=980)
    UTSerror = forms.FloatField(label='UTSerror (MPa)', initial=30)

    # Example:
    otherVariable = forms.FloatField(label='Label for the variable', initial=0.0)
    # The initial_value has to be set
```

These input variables are inserted when the user enters the page. The form part in the HTML template is the following:

```html
<div id="container">
  <h1>Spring UTS Analysis</h1>
  <form method="post">
    {% csrf_token %} {{ form.as_p }}
    <button type="submit">Generate Analysis</button>
  </form>
</div>
```

The double brackets (`{{ }}`) indicate that it is waiting for a variable sent from the server.

2. **Read data and send a response in `main.py`:**

   - The form is processed in `main.py`. Below is the code to read the new variable created and to send the result (or results) as required:

```python
def main(request):
    if request.method == 'POST':
        form = springUTS_Form(request.POST)
        if form.is_valid():
            # Get parameters from the form
            springDiameter = form.cleaned_data['springDiameter']
            wireDiameter = form.cleaned_data['wireDiameter']
            activeCoils = form.cleaned_data['activeCoils']
            length = form.cleaned_data['length']
            UTS = form.cleaned_data['UTS']
            UTSerror = form.cleaned_data['UTSerror']

            # Example for the new variable
            otherVariable = form.cleaned_data['otherVariable']

            # Example of an operation with the new variable
            newResult = otherVariable * 2

            my_spring = springUTS.springUTS(springDiameter=springDiameter,
                wireDiameter=wireDiameter, activeCoils=activeCoils,
                length=length, UTS=UTS, UTSerror=UTSerror)

            factor = my_spring.calcFactor()
            stress_absorbed = my_spring.stress_absorbed_by_spring()
            result1, result2, result3, result4 = my_spring.results()
            error1, error2, error3, error4 = my_spring.calcErrors()
            image_base64 = my_spring.plot()

            return render(request, 'springUTS.html', {
                                    'form': form,
                                    'factor': round(factor, 2),
                                    'stress_absorbed': round(stress_absorbed, 2),
                                    'result1': round(result1, 2),
                                    'result2': round(result2, 2),
                                    'result3': round(result3, 2),
                                    'result4': round(result4, 2),
                                    'error1': round(error1, 2),
                                    'error2': round(error2, 2),
                                    'error3': round(error3, 2),
                                    'error4': round(error4, 2),
                                    'newResult': newResult,  # Example of the response
                                    'image_base64': image_base64,
                                })
    else:
        form = springUTS_Form()

    return render(request, 'springUTS.html', {'form': form})
```

To show the user the result, the HTML must be specified to receive that result.

```html
{% if factor %}
<div class="results">
  <h2>Results</h2>
  <p><strong>Ultimate Stress Correlation Factor:</strong> {{ factor }}</p>
  <p>
    <strong>Stress Absorbed by the Spring (MPa):</strong> {{ stress_absorbed }}
  </p>
  <p>
    <strong>Material UTS:</strong> {{ result1 }} MPa &plusmn; {{ error1 }} MPa
  </p>
  <p>
    <strong>Material Fatigue Limit:</strong> {{ result2 }} MPa &plusmn; {{
    error2 }} MPa
  </p>
  <p>
    <strong>Material + Spring UTS:</strong> {{ result3 }} MPa &plusmn; {{ error3
    }} MPa
  </p>
  <p>
    <strong>Material + Spring Fatigue Limit:</strong> {{ result4 }} MPa &plusmn;
    {{ error4 }} MPa
  </p>
  <!-- Result Example -->
  <p>{{ newResult }}</p>
</div>
{% endif %}
```

The `if` clause ensures that results are displayed only if they are sent.

# Plot Generation (send an image)

The approach taken for visualizing the system was to use `matplotlib` to create the plot and then convert it into a binary format. The relevant code for this process is in `stability/views_module/process_object_and_render.py`.

### Overview of `process_object_and_render()`

The `process_object_and_render()` function performs the following steps:

1. **Initialize Plot**  
   A `matplotlib` plot is initialized.

2. **Generate Plots**  
   The required system plots are created using the provided data and modules of the project.

3. **Convert Plot to Binary**  
   The plot is saved in SVG format and encoded into a Base64 string. This string is stored in the `svg_base64` variable.

4. **Send to Frontend**  
   The `svg_base64` variable is passed to the frontend via the context (is a dictionary of variables to be send).

### Code Snippet

```python
def process_object_and_render(request, template, context):

    max_rotation = request.session.get('max_rotation')
    object_data = request.session.get('object_data')
    angle_session = request.session.get('angle')
    roll_center = request.session.get('roll_center')
    gravity_center_val = request.session.get('gravity_center_val')

    distance = compute_distance(np.array(roll_center), np.array(gravity_center_val))
    request.session['distance'] = float(distance)

    # Initialize plot
    fig, ax = plt.subplots()

    # Create system object, set theta as the inputted value, and compute omega
    object = system_object(**object_data)
    object.theta = angle_session
    omega(object)

    # Plot system and configure plot settings
    frontStability.plot_system(object, gravity_center_val, fig, ax)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.ylim(-0.1, 0.8)
    plt.xlim(-1.2, 1.2)

    # Save plot as SVG and encode in Base64
    buffer = io.BytesIO()
    plt.savefig(buffer, bbox_inches='tight', format='svg')
    buffer.seek(0)
    svg_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    # Update context with computed values and SVG data
    context.update({
        'svg_base64': svg_base64,
        'roll_center_x': round(roll_center[0], 3),
        'roll_center_y': round(roll_center[1], 3),
        'gravity_center_x': round(gravity_center_val[0], 3),
        'gravity_center_y': round(gravity_center_val[1], 3),
        'max_rotation': round(np.rad2deg(max_rotation), 3),
        'distance': round(distance, 3)
    })

    table_data = request.session.get('table_data')
    context.update({
        'table_data': json.dumps(table_data)  # Pass data as JSON to the template
    })

    # Render and return the response
    return render(request, template, context)

After the base64 image is send, the line 61, of stability.html template shows how the image is received:

<img id="roll-center-image" src="data:image/svg+xml;base64,{{ svg_base64 }}" alt="Suspension Image">
```
