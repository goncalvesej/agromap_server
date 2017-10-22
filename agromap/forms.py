from django import forms

from agromap_api.models.user import User

class FormLogin(forms.Form):
    email = forms.CharField(
        label='Email',
        max_length=40,
        widget=forms.TextInput(attrs=
            {
                'id':'email',
                'name':'email',
                'placeholder':'Email',
                'class': 'form-control',
                'required':'required'
            }
        )
    )
    password = forms.CharField(
        label='Senha',
        max_length=255,
        widget=forms.TextInput(attrs=
            {
                'id':'password',
                'name':'password',
                'placeholder':'Senha',
                'class': 'form-control',
                'type': 'password',
                'required':'required'
            }
        )
    )
