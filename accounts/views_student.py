from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.models import User, Administrator, Staff, Student, Session, ClassLevel, Subject
from accounts.forms import AddStudentForm, EditStudentForm

def home(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)
    student = user.student
    # data used in every view
    request.session['user_school_id'] = user.school_id
    request.session['user_first_name'] = user.first_name
    request.session['user_last_name'] = user.last_name
    request.session['user_other_names'] = user.other_names

    subjects = student.class_level.subject_set.all()

    context = {
        'user_school_id': request.session.get('user_school_id'),
        'user_first_name': request.session.get('user_first_name'),
        'user_last_name': request.session.get('user_last_name'),
        'user_other_names': request.session.get('user_other_names'),
        "subjects": subjects
    }

    return render(request, "student_templates/home_template.html", context)

def profile(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)
    student = user.student

    context={
        "user": user,
        'user_school_id': request.session.get('user_school_id'),
        'user_first_name': request.session.get('user_first_name'),
        'user_last_name': request.session.get('user_last_name'),
        'user_other_names': request.session.get('user_other_names'),
        "student": student,
        "gender_data": user.gender_data,
    }
    return render(request, 'student_templates/student_profile.html', context)
    

def edit_profile(request, user_school_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("/" + user_school_id + '/student_profile')

    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        other_names = request.POST.get('other_names')
        password = request.POST.get('password')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        try:
            user = User.objects.get(school_id=user_school_id)
            user.first_name = first_name
            user.last_name = last_name
            user.other_names = other_names
            user.email = email
            user.gender = gender
            user.phone_number = phone_number
            user.student.address = address

            if password != None and password != "":
                user.set_password(password)
            user.save()

            messages.success(request, "Profile Updated Successfully")

        except:
            messages.error(request, "Failed to Update Profile")

        finally:
            return redirect("/" + user_school_id + '/student_profile')