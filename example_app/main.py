# Django function to send a response to the frontend
from django.shortcuts import render
# Import the class from the custom module (functionalities)
from .modules.example_functions import example_class

# Import the forms (input fields)
from example_app.forms import example_Form, example_Form_2


def main(request):
    """
    This function handles user interactions and sends a response to the frontend.

    Args:
        request: A Django HttpRequest object.

    Returns:
        A Django HttpResponse object with the rendered template and data.
    """

    # Check if the user submitted a POST request (with data)
    if request.method == 'POST':
        # Check if the request data contains 'example' to implement logic
        if 'example' in request.POST:
            # Create a form to retrieve data from the request
            form = example_Form(request.POST)

            # Validate the form data
            if form.is_valid():
                # Extract the 'example' parameter from the validated form data
                example = form.cleaned_data['example']

                # Create an object of the example_class
                example_object = example_class(example=example)

                # Call a method on the object to get a result
                result = example_object.double()

                # Save the result in the session data (shared storage)
                request.session['result'] = result

                # Render the template with the forms and the result
                return render(request, 'example.html', {
                    'form': example_Form(),
                    'form2': example_Form_2(),
                    'result': round(result, 2),
                })

        # Check if the request data contains 'example2' to implement logic
        if 'example2' in request.POST:
            # Create a form to retrieve data from the request
            form = example_Form_2(request.POST)

            # Validate the form data
            if form.is_valid():
                # Get the previously saved "result" from the session data
                result = request.session.get('result')

                # Extract the 'example2' parameter from the validated form data
                example2 = form.cleaned_data['example2']

                # Perform operations using the retrieved result and the new data
                result2 = example2 * result

                # Render the template with the forms and both results
                return render(request, 'example.html', {
                    'form': example_Form(),
                    'form2': example_Form_2(),
                    'result': round(result, 2),
                    'result2': round(result2, 2),
                })

    # Render the initial forms if the request is not a POST request
    return render(request, 'example.html', {
        'form': example_Form(),
        'form2': example_Form_2(),
    })