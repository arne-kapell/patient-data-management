from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from pdm.models import Document, Note, AccessRequest, User, VerificationRequest
from pdm.forms import CustomUserCreationForm, CustomUserChangeForm

admin.site.register(Document)
admin.site.register(Note)
admin.site.register(AccessRequest)
admin.site.register(VerificationRequest)


class CustomUserAdmin(UserAdmin):
    add_form: CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'role', 'verified', 'first_name',
                    'last_name', 'is_staff', 'is_active',)
    list_filter = ('email', 'role', 'verified', 'first_name',
                   'last_name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
        ('Permissions', {
         'fields': ('role', 'verified', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'verified', 'password1', 'password2', 'first_name', 'last_name')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)

admin.site.site_header = "PDM Administration"
