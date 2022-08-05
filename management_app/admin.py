from django.contrib import admin

# Register your models here.

from .models import CustomUser, Administrator, Staff, Student, Session, ClassLevel, Subject

admin.site.register(CustomUser)
admin.site.register(Administrator)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Session)
admin.site.register(ClassLevel)
admin.site.register(Subject)