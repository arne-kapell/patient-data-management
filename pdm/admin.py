from django.contrib import admin
# from django.contrib.auth.models import Permission
from .models import Document, Note, AccessRequest, User

admin.site.register(Document)
admin.site.register(Note)
admin.site.register(AccessRequest)

# admin.site.register(Permission)
admin.site.register(User)

admin.site.site_header = "PDM Administration"
