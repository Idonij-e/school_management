from dataclasses import fields
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import User, Administrator, Staff, Student, Session, ClassLevel, Subject

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ( 'school_id', 'email', 'username', 'password')}),
        ("Personal Info", {'fields': ('last_name', 'first_name', 'other_names')}),
        ("Permissions", {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ("Important Dates", {'fields': ('last_login', 'date_joined')})
    )

    readonly_fields = ['school_id']

    add_fieldsets = (
        ('Auth Field', {"fields": ('email', 'username', 'password1', 'password2')}),
    )

# admin.site.register(User, CustomUserAdmin)
admin.site.register(User)
admin.site.register(Administrator)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Session)
admin.site.register(ClassLevel)
admin.site.register(Subject)