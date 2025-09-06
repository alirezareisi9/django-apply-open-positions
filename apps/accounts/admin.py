from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

@admin.register(models.CustomUser)
class UserAdmin(admin.ModelAdmin) :
    fieldsets = [
        (
            'User Information',  # Name of collection of these fields on admin panel
            {
                'fields': ['email', 'password', 'first_name', 'last_name', 'major', 
                'field', 'is_active', 'is_superuser', 'is_staff'],
            },
        ),
    ]
    list_display = ('email', 'first_name', 'last_name', 'major', 'field')  # display of any instance in list
    list_filter = ('major',)  # filter of any instance in list
