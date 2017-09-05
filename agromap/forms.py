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



class FormUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'last_name', 'email', 'password']
        widgets = {
            'name': forms.TextInput(attrs=
                {
                    'id':'name',
                    'name':'name',
                    'placeholder':'Nome',
                    'class':'form-control'
                }
            ),
            'last_name': forms.TextInput(attrs=
                {
                    'id':'last_name',
                    'name':'last_name',
                    'placeholder':'Sobrenome',
                    'class':'form-control'
                }
            ),
            'email': forms.TextInput(attrs=
                {
                    'id':'email',
                    'name':'email',
                    'placeholder':'Email',
                    'class':'form-control'
                }
            ),
            'password': forms.TextInput(attrs=
                {
                    'id':'passoword',
                    'name':'passoword',
                    'placeholder':'Senha',
                    'type':'password',
                    'class':'form-control'
                }
            ),
        }
