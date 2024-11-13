from django import forms

class springUTS_Form(forms.Form):
    springDiameter = forms.FloatField(label='Spring Diameter (mm)', initial=11.2)
    wireDiameter = forms.FloatField(label='Wire Diameter (mm)', initial=0.8)
    activeCoils = forms.IntegerField(label='Active Coils', initial=20)
    length = forms.FloatField(label='Length (mm)', initial=40)
    UTS = forms.FloatField(label='UTS (MPa)', initial=980)
    UTSerror = forms.FloatField(label='UTSerror (MPa)', initial=30)
