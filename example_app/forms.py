from django import forms

class example_Form(forms.Form):
    example = forms.FloatField(label='Example Variable', initial=1)