from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class SchoolSession(models.Model):
    id = models.AutoField(primary_key=True)
    start = models.DateField()
    end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.start) + " ---------- " + str(self.end)
    
    
class ClassLevel(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.class_name

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    class_level = models.ForeignKey(ClassLevel,on_delete=models.DO_NOTHING)
    school_session = models.ForeignKey(SchoolSession,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    class_level = models.ForeignKey(ClassLevel,on_delete=models.CASCADE,default=1)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_name + " " + self.class_level.class_name

@receiver(post_save,sender=CustomUser)
def add_user_to_group(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Administrator.objects.create(user=instance)
        if instance.user_type==2:
            Staff.objects.create(user=instance)
        if instance.user_type==3:
            Student.objects.create(
                user=instance,
                class_level=ClassLevel.objects.get(id=1),
                school_session=SchoolSession.objects.get(id=1)
            )
            
@receiver(post_save,sender=CustomUser)
def save_user_to_group(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.administrator.save()
    if instance.user_type==2:
        instance.staff.save()
    if instance.user_type==3:
        instance.student.save()