import uuid
from django.db import models


def get_upload_path(instance, filename):
    return f"documents/{instance.owner.username}/{filename}"


class Document(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    pages = models.IntegerField()
    file = models.FileField(upload_to=get_upload_path)
    upload = models.DateTimeField(auto_now_add=True)
    sensitive = models.BooleanField(default=False)


class Note(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    page = models.IntegerField()
    text = models.TextField()


class AccessRequest(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True)
