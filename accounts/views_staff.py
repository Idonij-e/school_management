from django.shortcuts import render, redirect
from django.contrib import messages


from .models import ClassLevel, User, Staff, Student, Session, Subject



def home(request, user_school_id):

    user = User.objects.get(school_id=user_school_id)
    # data used in every view
    request.session['user_school_id'] = user.school_id
    request.session['user_first_name'] = user.first_name
    request.session['user_last_name'] = user.last_name
    request.session['user_other_names'] = user.other_names

    # Fetching All Students under Staff

    subjects = Subject.objects.filter(staff=user)
    class_level_list = []
    for subject in subjects:
        class_level = ClassLevel.objects.get(id=subject.class_level.id)
        class_level_list.append(class_level)
    
    students_count = Student.objects.filter(class_level__in=class_level_list).count()
    subject_count = subjects.count()


    context={
        'user': user,
        'user_school_id': request.session.get('user_school_id'),
        'user_first_name': request.session.get('user_first_name'),
        'user_last_name': request.session.get('user_last_name'),
        'user_other_names': request.session.get('user_other_names'),
        "students_count": students_count,
        "subject_count": subject_count,
    }

    return render(request, "staff_templates/home_template.html", context)


def profile(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)
    staff = user.staff

    context={
        "user": user,
        'user_school_id': request.session.get('user_school_id'),
        'user_first_name': request.session.get('user_first_name'),
        'user_last_name': request.session.get('user_last_name'),
        'user_other_names': request.session.get('user_other_names'),
        "staff": staff,
        "gender_data": user.gender_data,
    }
    return render(request, 'staff_templates/staff_profile.html', context)

def edit_profile(request, user_school_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("/" + user_school_id + '/staff_profile')

    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        other_names = request.POST.get('other_names')
        password = request.POST.get('password')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')

        try:
            user = User.objects.get(school_id=user_school_id)
            user.first_name = first_name
            user.last_name = last_name
            user.other_names = other_names
            user.email = email
            user.gender = gender
            user.phone_number = phone_number

            if password != None and password != "":
                user.set_password(password)
            user.save()

            messages.success(request, "Profile Updated Successfully")

        except:
            messages.error(request, "Failed to Update Profile")

        finally:
            return redirect("/" + user_school_id + '/staff_profile')