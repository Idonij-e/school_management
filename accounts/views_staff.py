import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt


from .models import ClassLevel, User, Staff, Student, Session, Subject, StudentResult



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


@csrf_exempt
def get_students(request):
    subject_id=request.POST.get("subject")
    session_year=request.POST.get("session_year")

    subject=Subject.objects.get(id=subject_id)
    #session_model=Session.object.get(id=session_year)
    students=Student.objects.filter(course_id=subject.course_id)
    list_data=[]

    for student in students:
        data_small={"id":student.user.school_id,"name":student.user.first_name+" "+student.user.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

def staff_add_result(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)
    #staff = user.staff
    subjects=Subject.objects.filter(staff=user)
    session_years=Session.object.all()
    context={
        'user_school_id': user_school_id,
        'user_first_name': request.session.get('user_first_name'),
        'user_last_name': request.session.get('user_last_name'),
        'user_other_names': request.session.get('user_other_names'),
        'subjects': subjects,
        'session_years': session_years,
    }
    return render(request, "staff_templates/staff_add_result.html", context)

def save_student_result(request, user_school_id):
    if request.method!='POST':
        #return HttpResponseRedirect('staff_add_result')
        return redirect("/" + user_school_id + '/staff_add_result')
    student_admin_id=request.POST.get('student_list')
    #assignment_marks=request.POST.get('assignment_marks')
    test_one_marks=request.POST.get('test_one_marks')
    test_two_marks=request.POST.get('test_two_marks')
    exam_marks=request.POST.get('exam_marks')
    subject_id=request.POST.get('subject')


    student_obj=Student.objects.get(user=student_admin_id)
    subject_obj=Subject.objects.get(id=subject_id)

    try:
        check_exist=StudentResult.objects.filter(subject=subject_obj,student=student_obj).exists()
        if check_exist:
            result=StudentResult.objects.get(subject=subject_obj,student=student_obj)
            #result.subject_assignment_marks=assignment_marks
            result.subject_test_one_marks=test_one_marks
            result.subject_test_two_marks=test_two_marks
            result.subject_exam_marks=exam_marks
            result.save()
            messages.success(request, "Successfully Updated Result")
            #return HttpResponseRedirect(reverse("staff_add_result"))
            return redirect("/" + user_school_id + '/staff_add_result')
        else:
            result=StudentResult(student=student_obj,subject=subject_obj,subject_exam_marks=exam_marks,subject_test_one_marks=test_one_marks,subject_test_two_marks=test_two_marks)
            result.save()
            messages.success(request, "Successfully Added Result")
            #return HttpResponseRedirect(reverse("staff_add_result"))
            return redirect("/" + user_school_id + '/staff_add_result')
    except:
        messages.error(request, "Failed to Add Result")
        #return HttpResponseRedirect(reverse("staff_add_result"))
        return redirect("/" + user_school_id + '/staff_add_result')

@csrf_exempt
def fetch_result_student(request):
    subject_id=request.POST.get('subject_id')
    student_id=request.POST.get('student_id')
    student_obj=Student.objects.get(user=student_id)
    result=StudentResult.objects.filter(student=student_obj.id,subject=subject_id).exists()
    if result:
        result=StudentResult.objects.get(student=student_obj.id,subject=subject_id)
        result_data={"exam_marks":result.subject_exam_marks,"test_one_marks":result.subject_test_one_marks,"test_two_marks":result.subject_test_two_marks}
        return HttpResponse(json.dumps(result_data))
    else:
        return HttpResponse("False")