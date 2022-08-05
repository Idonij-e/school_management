from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
def generate_pk():
    from .models import CustomUser
    from datetime import datetime
    year = datetime.now().year
    index = CustomUser.objects.filter(created_at__year__gte=year).count() + 100
    return "B{}".format(str(year)) + str(index)

class CustomUser(models.Model):
    user_type_data = ((1,"Administrator"),(2,"Staff"),(3,"Student"))
    user_type = models.IntegerField(default=1,choices=user_type_data)
    school_id = models.CharField(max_length=10, default=generate_pk, editable=False)
    profile_pic = models.ImageField(null=True, blank = True, upload_to = "images/")
    # name
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    other_names = models.CharField(max_length=32, blank=True, null=True)
    # contact
    email = models.EmailField(unique=True)  # require
    phone_numbers = models.PositiveIntegerField(blank=True, null=True)
    address = models.TextField(null=True, blank=True)

    # registration
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # bio
    gender_data = ((1, "Male"), (2, "Female"))
    gender = models.IntegerField(default=2, choices=gender_data)

    def __str__(self):
        return self.last_name + ' ' + self.first_name
    
class Administrator(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)

class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Session(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year=models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class ClassLevel(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.class_name

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    class_level = models.ForeignKey(ClassLevel,on_delete=models.DO_NOTHING)
    session_year = models.ForeignKey(Session,on_delete=models.CASCADE)



class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    class_level = models.ForeignKey(ClassLevel,on_delete=models.CASCADE,default=1)
    staff = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_name
