from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, Company


class ClientAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'name', 'group', 'surname', 'active', 'staff')
    list_filter = ('group', 'staff')
    fieldsets = (
        (None, {'fields': ('email', 'name', 'group', 'surname', 'active', 'staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'group', 'password1', 'password2', 'name', 'surname', 'active', 'staff')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, ClientAdmin)
admin.site.register(Company)
