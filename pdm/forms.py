from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

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
            'country'
            'postal_code', 
            'city', 
            'street_name', 
            'street_number', 
        )


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )
