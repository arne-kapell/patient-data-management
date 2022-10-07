# Generated by Django 4.1 on 2022-10-07 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uid", models.CharField(max_length=255, unique=True)),
                ("owner", models.CharField(max_length=255)),
                ("pages", models.IntegerField()),
                (
                    "file",
                    models.FileField(
                        upload_to="documents/<django.db.models.fields.CharField>"
                    ),
                ),
                ("upload", models.DateTimeField(auto_now_add=True)),
                ("sensitive", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Note",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uid", models.CharField(max_length=255, unique=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("page", models.IntegerField()),
                ("text", models.TextField()),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pdm.document"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AccessRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("requested_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.CharField(max_length=255)),
                ("approved", models.BooleanField(default=False)),
                ("approved_at", models.DateTimeField(null=True)),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pdm.document"
                    ),
                ),
            ],
        ),
    ]
