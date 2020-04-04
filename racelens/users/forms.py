from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput(), label='Contraseña')


class UserRegistrationForm(forms.Form):
    name = forms.CharField(
        required = True,
        label = 'Nombre'
    )
    last_name = forms.CharField(
        required = True,
        label = 'Apellido'
    )
    username = forms.CharField(
        required = True,
        label = 'Nombre de usuario',
        max_length = 32
    )
    email = forms.CharField(
        required = True,
        label = 'Correo',
        max_length = 32,
    )
    password = forms.CharField(
        required = True,
        label = 'Contraseña',
        max_length = 32,
        widget = forms.PasswordInput()
    )