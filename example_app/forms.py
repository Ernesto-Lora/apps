from django import forms

class example_Form(forms.Form):
    example = forms.FloatField(label='Example Variable', initial=1)

class example_Form_2(forms.Form):
    example2 = forms.FloatField(label='Example Variable 2', initial=3)