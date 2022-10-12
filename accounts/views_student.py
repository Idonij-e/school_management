from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.conf import settings

from accounts.models import (
    User,
    Administrator,
    Staff,
    Student,
    Session,
    ClassLevel,
    Subject,
    Fee,
    Payment,
    StudentAssessment,
)
from accounts.forms import AddStudentForm, EditStudentForm
from http.client import HTTPResponse

# for payment pdf generation
from django.template.loader import get_template
from xhtml2pdf import pisa


def home(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)
    student = user.student

    # data used in every view
    request.session["user_school_id"] = user.school_id
    request.session["user_first_name"] = user.first_name
    request.session["user_last_name"] = user.last_name
    request.session["user_other_names"] = user.other_names

    subjects = student.class_level.subject_set.all()
    course = ClassLevel.objects.get(id=student.class_level.id)
    fee_term_one = Fee.objects.filter(course_id=course, term="Term 1")
    fee_term_two = Fee.objects.filter(course_id=course, term="Term 2")
    fee_term_three = Fee.objects.filter(course_id=course, term="Term 3")
    fee_others = Fee.objects.filter(course_id=course, term="Not Term-related")

    context = {
        "user_school_id": request.session.get("user_school_id"),
        "user_first_name": request.session.get("user_first_name"),
        "user_last_name": request.session.get("user_last_name"),
        "user_other_names": request.session.get("user_other_names"),
        "subjects": subjects,
        "fee_term_one": fee_term_one,
        "fee_term_two": fee_term_two,
        "fee_term_three": fee_term_three,
        "fee_others": fee_others,
    }

    return render(request, "student_templates/home_template.html", context)


def profile(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)
    student = user.student

    subjects = student.class_level.subject_set.all()
    course = ClassLevel.objects.get(id=student.class_level.id)
    fee_term_one = Fee.objects.filter(course_id=course, term="Term 1")
    fee_term_two = Fee.objects.filter(course_id=course, term="Term 2")
    fee_term_three = Fee.objects.filter(course_id=course, term="Term 3")
    fee_others = Fee.objects.filter(course_id=course, term="Not Term-related")

    context = {
        "user": user,
        "user_school_id": request.session.get("user_school_id"),
        "user_first_name": request.session.get("user_first_name"),
        "user_last_name": request.session.get("user_last_name"),
        "user_other_names": request.session.get("user_other_names"),
        "student": student,
        "gender_data": user.gender_data,
        "fee_term_one": fee_term_one,
        "fee_term_two": fee_term_two,
        "fee_term_three": fee_term_three,
        "fee_others": fee_others,
    }
    return render(request, "student_templates/student_profile.html", context)


def edit_profile(request, user_school_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("/" + user_school_id + "/student_profile")

    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        other_names = request.POST.get("other_names")
        password = request.POST.get("password")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")

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
            return redirect("/" + user_school_id + "/student_profile")


def initiate_payment(request, user_school_id, fee_id):
    fee = Fee.objects.get(id=fee_id)
    user = User.objects.get(school_id=user_school_id)
    payment_model = Payment(fee_id=fee, student=user.student)
    current_session = Session.objects.get(current_session=True)
    payment_model.session = str(current_session).split(' ')[0]
    payment_model.save()
    student = user.student

    subjects = student.class_level.subject_set.all()
    course = ClassLevel.objects.get(id=student.class_level.id)
    fee_term_one = Fee.objects.filter(course_id=course, term="Term 1")
    fee_term_two = Fee.objects.filter(course_id=course, term="Term 2")
    fee_term_three = Fee.objects.filter(course_id=course, term="Term 3")
    fee_others = Fee.objects.filter(course_id=course, term="Not Term-related")

    context = {
        "user_first_name": request.session.get("user_first_name"),
        "user_last_name": request.session.get("user_last_name"),
        "user_other_names": request.session.get("user_other_names"),
        "user_school_id": user_school_id,
        "fee": fee,
        "payment": payment_model,
        "paystack_public_key": settings.PAYSTACK_PUBLIC_KEY,
        "fee_term_one": fee_term_one,
        "fee_term_two": fee_term_two,
        "fee_term_three": fee_term_three,
        "fee_others": fee_others,
    }
    return render(request, "student_templates/make_payment.html", context)


def verify_payment(request: HttpRequest, ref: str) -> HTTPResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "{} payment Successful".format(payment.fee_id.fee_name.title()))
        all_payments = Payment.objects.filter(verified=False)
        all_payments.delete()

    user_school_id = request.session.get("user_school_id")
    return redirect("/" + user_school_id + "/payment_history")
        

def payment_history(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)
    student = user.student
    course = ClassLevel.objects.get(id=student.class_level.id)
    payment_all = Payment.objects.filter(student=student, verified=True)
    fee_term_one = Fee.objects.filter(course_id=course, term="Term 1")
    fee_term_two = Fee.objects.filter(course_id=course, term="Term 2")
    fee_term_three = Fee.objects.filter(course_id=course, term="Term 3")
    fee_others = Fee.objects.filter(course_id=course, term="Not Term-related")

    context = {
        "user_first_name": request.session.get("user_first_name"),
        "user_last_name": request.session.get("user_last_name"),
        "user_other_names": request.session.get("user_other_names"),
        "user_school_id": user_school_id,
        "payment_all": payment_all,
        "course": course,
        "fee_term_one": fee_term_one,
        "fee_term_two": fee_term_two,
        "fee_term_three": fee_term_three,
        "fee_others": fee_others,
    }
    return render(request, "student_templates/payment_history.html", context)


def payment_pdf(request, *args, **kwargs):
    ref = kwargs.get("ref")
    payment = get_object_or_404(Payment, ref=ref)
    sessions = Session.objects.all()
    template_path = "student_templates/payment_pdf.html"
    context = {"payment": payment, "sessions": sessions}

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="payment.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    # return response
    return render(request, template_path, context)


def student_view_result(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)
    # student=Student.objects.get(user=request.user.id)
    studentresult = StudentResult.objects.filter(student=user.id)

    context = {
        "user_first_name": request.session.get("user_first_name"),
        "user_last_name": request.session.get("user_last_name"),
        "user_other_names": request.session.get("user_other_names"),
        "user_school_id": user_school_id,
        "studentresult": studentresult,
    }
    return render(request, "student_templates/student_result.html", context)

def payment_status(request, payment_ref):
    return HttpResponse('successfully, payment reference: ' + payment_ref)
