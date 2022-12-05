from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from pdm.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'role', 'verified', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'role', 'verified', 'first_name', 'last_name')


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
        )


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )
