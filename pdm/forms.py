from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from pdm.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'role', 'verified', 'first_name', 'last_name', 'birth_date', 
        'sex', 'phone', 'street_name', 'street_number', 'city', 'postal_code', 'country')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'role', 'verified', 'first_name', 'last_name', 'birth_date', 
        'sex', 'phone', 'street_name', 'street_number', 'city', 'postal_code', 'country')


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'birth_date', 
            'sex', 
            'phone', 
            'country',
            'postal_code', 
            'city', 
            'street_name', 
            'street_number'
        )


class ChangeableForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)
    country = forms.CharField(required=False)
    postal_code = forms.CharField(required=False)
    city = forms.CharField(required=False)
    street_name = forms.CharField(required=False)
    street_number = forms.CharField(required=False)
    class Meta:
        model = User
        fields = (
            'email', 
            'phone', 
            'country',
            'postal_code', 
            'city', 
            'street_name', 
            'street_number'
        )



class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )
