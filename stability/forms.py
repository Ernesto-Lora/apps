from django import forms
from django.utils.safestring import mark_safe
import numpy as np
from django.forms import formset_factory

class SuspensionForm(forms.Form):
    D = forms.FloatField(label='D (m)', initial=1.7)
    Dtw = forms.FloatField(label=mark_safe('D<sub>tw</sub> (m)'), initial=0.15)
    ht = forms.FloatField(label=mark_safe('h<sub>t</sub> (m)'), initial=0.7)
    hu = forms.FloatField(label= mark_safe('h<sub>u</sub> (m)'), initial=0.5)
    hb = forms.FloatField(label= mark_safe('h<sub>b</sub> (m)'), initial=0.25)
    lu = forms.FloatField(label= mark_safe('l<sub>u</sub> (m)'), initial=0.2)
    lb = forms.FloatField(label= mark_safe('l<sub>b</sub> (m)'), initial=0.25)
    philu = forms.IntegerField(label=mark_safe('Φ<sub>lu</sub> ( °)'), initial=85)
    philb = forms.IntegerField(label=mark_safe('Φ<sub>lb</sub> ( °)') , initial=81)
    phiru = forms.IntegerField(label=mark_safe('Φ<sub>ru</sub> ( °)'), initial=85)
    phirb = forms.IntegerField(label=mark_safe('Φ<sub>rb</sub> ( °)'), initial=81)

class thetaForm(forms.Form):
    angle = forms.IntegerField(label=' θ ( °)', initial=0)

    def __init__(self, max_rotation=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_rotation = max_rotation

    def clean_angle(self):
        angle = self.cleaned_data['angle']
        if self.max_rotation is not None and angle > np.rad2deg(self.max_rotation):
            raise forms.ValidationError(f"Angle must be less than or equal to {self.max_rotation}.")
        return angle
    
class radius_form(forms.Form):
    distance = forms.FloatField(label='Distance Between Roll center and Gravity Center (m)', initial=0.1)
    radius = forms.FloatField(label='Curve radius R (m)', initial=400)

class velocity_form(forms.Form):
    distance = forms.FloatField(label='Distance Between Roll center and Gravity Center (m)', initial=0.1)
    radius_for_rotation = forms.FloatField(label='Curve radius R (m)', initial=400)
    velocity = forms.FloatField(label=' v (km/h)', initial=100)
    k = forms.FloatField(label=' K (N/m)', initial=12000)
