from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.core.validators import RegexValidator
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
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}), required=True, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Repeat Password'}), required=True, label="Repeat Password")
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    birth_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date'}), required=True)
    sex = forms.ChoiceField(choices=[
        ("", ""),
        ("m", "Male"),
        ("f", "Female"),
        ("d", "Diverse")
    ], validators=[RegexValidator(regex=r'^[mfd]$', message="Please select a valid sex")], required=True)
    phone = forms.CharField(required=True, validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")], widget=forms.TextInput(attrs={'placeholder': '+999999999'}))
    country = forms.CharField(required=True, validators=[
        RegexValidator(regex=r'^[A-Z]{2}$', message="Country must be entered in the format: 'XX'.")], widget=forms.TextInput(attrs={'placeholder': 'e.g. DE'}))
    postal_code = forms.CharField(required=True, validators=[
        RegexValidator(regex=r'^[0-9]{5}$', message="Postal code must be entered in the format: '99999'.")], widget=forms.TextInput(attrs={'placeholder': 'e.g. 12345'}))
    city = forms.CharField(required=True)
    street_name = forms.CharField(required=True)
    street_number = forms.CharField(required=True)

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
    phone = forms.CharField(required=False, validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")], widget=forms.TextInput(attrs={'placeholder': '+999999999'}))
    country = forms.CharField(required=False, validators=[
        RegexValidator(regex=r'^[A-Z]{2}$', message="Country must be entered in the format: 'XX'.")], widget=forms.TextInput(attrs={'placeholder': 'e.g. DE'}))
    postal_code = forms.CharField(required=False, validators=[
        RegexValidator(regex=r'^[0-9]{5}$', message="Postal code must be entered in the format: '99999'.")], widget=forms.TextInput(attrs={'placeholder': 'e.g. 12345'}))
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
