# Generated by Django 4.1 on 2022-12-02 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pdm", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="accessrequest",
            old_name="approved_at",
            new_name="approved_or_denied_at",
        ),
        migrations.AddField(
            model_name="accessrequest",
            name="denied",
            field=models.BooleanField(default=False),
        ),
    ]