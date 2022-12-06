import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from pdm.managers import UserManager
from pdm.tools import getUsersDocFolder


def get_upload_path(instance: any, filename: str) -> str:
    return f"{getUsersDocFolder(instance.owner)}{instance.uid}.{filename.split('.')[-1]}"


class Document(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    pages = models.IntegerField(default=0)
    file = models.FileField(upload_to=get_upload_path)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    sensitive = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.file.delete()
        return super().delete(*args, **kwargs)


class Note(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    page = models.IntegerField()
    text = models.TextField()


class AccessRequest(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name="patient")
    requested_at = models.DateTimeField(auto_now_add=True)
    requested_by = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name="doctor")
    period_start = models.DateField()
    period_end = models.DateField()
    approved = models.BooleanField(default=False)
    denied = models.BooleanField(default=False)
    approved_or_denied_at = models.DateTimeField(null=True)


class VerificationRequest(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    target_user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name="target_user")
    medical_role = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    hints = models.TextField(blank=True)
    check_url = models.URLField(null=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    denied = models.BooleanField(default=False)
    reason = models.TextField(null=True)
    processed_at = models.DateTimeField(null=True)
    processed_by = models.ForeignKey(
        'User', on_delete=models.CASCADE, null=True, related_name="processed_by")


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    sex = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    # address
    street_name = models.CharField(max_length=255, null=True)
    street_number = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    postal_code = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Role choices
    PATIENT = 1
    DOCTOR = 2
    VERIFICATOR = 3

    ROLES = (
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
        (VERIFICATOR, 'Verificator')
    )

    role = models.PositiveSmallIntegerField(choices=ROLES, default=PATIENT)
    verified = models.BooleanField(default=False)

    objects = UserManager()

    # def save(self, *args, **kwargs):
    #     if self.role == User.VERIFICATOR:
    #         self.is_staff = True  # TODO: remove and implement in UI
    #     elif not self.is_superuser:
    #         self.is_staff = False
    #     super().save(*args, **kwargs)
