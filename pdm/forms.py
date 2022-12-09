from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.conf import settings
from django import forms
from django.utils.translation import gettext_lazy as _

from pdm.models import Document, User


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


class UserInfoEditForm(forms.ModelForm):
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


class DeleteAccountForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )


def validate_file_extension(file):
    from django.core.exceptions import ValidationError
    ext = file.name.split('.')[-1]
    valid_extensions: list = settings.ACCEPTED_DOCUMENT_EXTENSIONS
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class DocumentUploadForm(forms.ModelForm):
    file = forms.FileField(max_length=settings.MAX_DOCUMENT_SIZE, widget=forms.ClearableFileInput(
        attrs={'multiple': False}), validators=[validate_file_extension])
    description = forms.CharField(
        max_length=255, required=False, widget=forms.Textarea(attrs={'rows': 3}))
    sensitive = forms.BooleanField(
        required=False, initial=False, widget=forms.CheckboxInput())

    class Meta:
        model = Document
        fields = (
            'file',
            'description',
            'sensitive'
        )


class DocumentUpdateForm(DocumentUploadForm):
    # description = None
    sensitive = None
