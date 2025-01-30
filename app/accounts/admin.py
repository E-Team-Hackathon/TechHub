from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        "is_staff",
        "is_active",
    )

    search_fields = ('username',)

    ordering = ('username',) 

    fieldsets = (('User Info', {'fields': ('username', 'password')}),)

    add_fieldsets = (
        (
            None,
            {
                'fields': ('username', 'password1', 'password2'),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)