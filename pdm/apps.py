from django.apps import AppConfig


class PdmConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pdm"

    # Create groups and permissions
    # def create_groups(sender, **kwargs):
    #     from django.contrib.auth.models import Permission, Group
    #     from django.contrib.contenttypes.models import ContentType
    #     patient, _ = Group.objects.get_or_create(name='Patient')
    #     doctor, _ = Group.objects.get_or_create(name='Doctor')
    #     verifyHelper, _ = Group.objects.get_or_create(name='VerifyHelper')

    #     patient.permissions.add(Permission.objects.filter(content_type=ContentType(
    #         app_label='pdm', model='accessrequest')).get(codename='view_accessrequest'))

    # def ready(self):
    #     from django.db.models.signals import post_migrate
    #     post_migrate.connect(self.create_groups, sender=self)
