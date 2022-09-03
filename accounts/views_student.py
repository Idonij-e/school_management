from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.conf import settings

from accounts.models import User, Administrator, Staff, Student, Session, ClassLevel, Subject, Fee, Payment
from accounts.forms import AddStudentForm, EditStudentForm
from http.client import HTTPResponse


def home(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)
    student = user.student
    
    # data used in every view
    request.session['user_school_id'] = user.school_id
    request.session['user_first_name'] = user.first_name
    request.session['user_last_name'] = user.last_name
    request.session['user_other_names'] = user.other_names

    subjects = student.class_level.subject_set.all()
    course=ClassLevel.objects.get(id=student.class_level.id)
    fee_term_one = Fee.objects.filter(course_id=course, term ='Term 1')
    fee_term_two = Fee.objects.filter(course_id=course, term ='Term 2')
    fee_term_three = Fee.objects.filter(course_id=course, term ='Term 3')
    fee_others = Fee.objects.filter(course_id=course, term ='Not Term-related')

    context = {
        'user_school_id': request.session.get('user_school_id'),
        'user_first_name': request.session.get('user_first_name'),
        'user_last_name': request.session.get('user_last_name'),
        'user_other_names': request.session.get('user_other_names'),
        "subjects": subjects,
        "fee_term_one":fee_term_one,
        "fee_term_two":fee_term_two,
        "fee_term_three":fee_term_three,
        "fee_others":fee_others
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

def initiate_payment(request, user_school_id, fee_id):
    fee = Fee.objects.get(custom_id=fee_id)
    payment_model = Payment(fee_id=fee)
    payment = payment_model.save()

    context = { 
        'user_first_name': request.session.get('user_first_name'),
        'user_last_name': request.session.get('user_last_name'),
        'user_other_names': request.session.get('user_other_names'),
        "user_school_id": user_school_id,
        'fee':fee,
        'payment': payment,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
        }
    return render(request,"student_template/make_payment.html", context)

def verify_payment(request: HttpRequest, ref: str) -> HTTPResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "Verification Successful")
    else:
        messages.error(request, "Verification Failed.")
    return redirect('initiate-payment')


