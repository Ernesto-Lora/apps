from django import forms
from django.utils.safestring import mark_safe

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
    theta = forms.IntegerField(label=' θ ( °)', initial=0)
