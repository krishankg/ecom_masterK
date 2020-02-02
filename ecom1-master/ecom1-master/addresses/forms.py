from django import forms

from .models import AddressModel

class AddressForm(forms.ModelForm):
    class Meta:
        model=AddressModel
        fields=['address_line_1','address_line_2','city','district','state','country','postal_code']
