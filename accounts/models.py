from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import generate_school_id
from .managers import UserManager



# Overriding the Default Django Auth User and adding One More Field (user_type)
class User(AbstractUser):
    school_id = models.CharField(default=generate_school_id, max_length=100, editable=False)
    user_type_data = (
        (1, "Administrator"), 
        (2, "Staff"), 
        (3, "Student")
        )
    user_type = models.PositiveIntegerField(default=1, choices=user_type_data)
    other_names = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    profile_pic = models.CharField(blank=True, null=True, max_length=10000)
    gender_data = (
        (1, "Female"),
        (2, "Male")
    )
    gender = models.PositiveIntegerField(default=1, choices=gender_data)
    phone_number = models.IntegerField(blank=True, null=True)

    objects = UserManager()



class Administrator(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.school_id + " " +  self.user.last_name +  self.user.first_name


class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.school_id + " " +  self.user.last_name +  self.user.first_name


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()

    def __str__(self) -> str:
        str(self.session_start_year) + " to " + str(self.session_end_year)



class ClassLevel(models.Model):
    id = models.AutoField(primary_key=True)
    class_level_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
	    return self.class_level_name



class Subject(models.Model):
    id =models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_name + " " + self.class_level.class_level_name



class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    address = models.TextField()
    class_level = models.ForeignKey(ClassLevel, on_delete=models.DO_NOTHING, default=1)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.school_id + " " +  self.user.last_name +  self.user.first_name




#Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=User)
# Now Creating a Function which will automatically insert data in Administrator, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            Administrator.objects.create(user=instance)
        if instance.user_type == 2:
            Staff.objects.create(user=instance)
        if instance.user_type == 3:
            Student.objects.create(user=instance, course_id=ClassLevel.objects.get(id=1), session_year_id=Session.objects.get(id=1))
    

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.administrator.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
    


