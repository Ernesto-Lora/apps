from django.shortcuts import render
from .modules import springUTS
# Create your views here.

import io
import base64
import pandas as pd
from springUTS.forms import springUTS_Form


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
                                    'image_base64': image_base64,
                                })
    else:
        form = springUTS_Form()

    return render(request, 'springUTS.html', {'form': form})