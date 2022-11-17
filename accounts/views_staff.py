import json
from multiprocessing import context

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from accounts.utils import current_term


from .models import (
    ClassLevel,
    User,
    Staff,
    Student,
    Session,
    Subject,
    StudentAssessment,
    Term,
)


def home(request, user_school_id):

    user = User.objects.get(school_id=user_school_id)
    # data used in every view
    request.session["user_school_id"] = user.school_id
    request.session["user_first_name"] = user.first_name
    request.session["user_last_name"] = user.last_name
    request.session["user_other_names"] = user.other_names
    # request.session['user_profile_pic'] = user.profile_pic

    # Fetching All Students under Staff

    subjects = Subject.objects.filter(staff=user)
    class_level_list = []
    for subject in subjects:
        class_level = ClassLevel.objects.get(id=subject.class_level.id)
        class_level_list.append(class_level)

    students_count = Student.objects.filter(class_level__in=class_level_list).count()
    subject_count = subjects.count()

    context = {
        "user": user,
        "user_school_id": request.session.get("user_school_id"),
        "user_first_name": request.session.get("user_first_name"),
        "user_last_name": request.session.get("user_last_name"),
        "user_other_names": request.session.get("user_other_names"),
        "students_count": students_count,
        "subject_count": subject_count,
        "subjects": subjects,
    }

    return render(request, "staff_templates/home_template.html", context)


def profile(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)
    staff = user.staff

    context = {
        "user": user,
        "user_school_id": request.session.get("user_school_id"),
        "user_first_name": request.session.get("user_first_name"),
        "user_last_name": request.session.get("user_last_name"),
        "user_other_names": request.session.get("user_other_names"),
        "staff": staff,
        "gender_data": user.gender_data,
    }
    return render(request, "staff_templates/staff_profile.html", context)


def edit_profile(request, user_school_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("/" + user_school_id + "/staff_profile")

    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        other_names = request.POST.get("other_names")
        password = request.POST.get("password")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        profile_pic = request.FILES.get("profile_pic")

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

            if profile_pic != None or profile_pic != "":
                user.profile_pic = profile_pic

            user.save()

            messages.success(request, "Profile Updated Successfully")

        except:
            messages.error(request, "Failed to Update Profile")

        finally:
            return redirect("/" + user_school_id + "/staff_profile")


@csrf_exempt
def get_students(request):
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year")

    subject = Subject.objects.get(id=subject_id)
    # session_model=Session.object.get(id=session_year)
    students = Student.objects.filter(course_id=subject.course_id)
    list_data = []

    for student in students:
        data_small = {
            "id": student.user.school_id,
            "name": student.user.first_name + " " + student.user.last_name,
        }
        list_data.append(data_small)
    return JsonResponse(
        json.dumps(list_data), content_type="application/json", safe=False
    )


def save_student_resultd(request, user_school_id):
    if request.method != "POST":
        # return HttpResponseRedirect('staff_add_result')
        return redirect("/" + user_school_id + "/staff_add_result")
    student_admin_id = request.POST.get("student_list")
    # assignment_marks=request.POST.get('assignment_marks')
    test_one_marks = request.POST.get("test_one_marks")
    test_two_marks = request.POST.get("test_two_marks")
    exam_marks = request.POST.get("exam_marks")
    subject_id = request.POST.get("subject")

    student_obj = Student.objects.get(user=student_admin_id)
    subject_obj = Subject.objects.get(id=subject_id)

    try:
        check_exist = StudentResult.objects.filter(
            subject=subject_obj, student=student_obj
        ).exists()
        if check_exist:
            result = StudentResult.objects.get(subject=subject_obj, student=student_obj)
            # result.subject_assignment_marks=assignment_marks
            result.subject_test_one_marks = test_one_marks
            result.subject_test_two_marks = test_two_marks
            result.subject_exam_marks = exam_marks
            result.save()
            messages.success(request, "Successfully Updated Result")
            # return HttpResponseRedirect(reverse("staff_add_result"))
            return redirect("/" + user_school_id + "/staff_add_result")
        else:
            result = StudentResult(
                student=student_obj,
                subject=subject_obj,
                subject_exam_marks=exam_marks,
                subject_test_one_marks=test_one_marks,
                subject_test_two_marks=test_two_marks,
            )
            result.save()
            messages.success(request, "Successfully Added Result")
            # return HttpResponseRedirect(reverse("staff_add_result"))
            return redirect("/" + user_school_id + "/staff_add_result")
    except:
        messages.error(request, "Failed to Add Result")
        # return HttpResponseRedirect(reverse("staff_add_result"))
        return redirect("/" + user_school_id + "/staff_add_result")


@csrf_exempt
def fetch_result_student(request):
    subject_id = request.POST.get("subject_id")
    student_id = request.POST.get("student_id")
    student_obj = Student.objects.get(user=student_id)
    result = StudentResult.objects.filter(
        student=student_obj.id, subject=subject_id
    ).exists()
    if result:
        result = StudentResult.objects.get(student=student_obj.id, subject=subject_id)
        result_data = {
            "exam_marks": result.subject_exam_marks,
            "test_one_marks": result.subject_test_one_marks,
            "test_two_marks": result.subject_test_two_marks,
        }
        return HttpResponse(json.dumps(result_data))
    else:
        return HttpResponse("False")


def view_subjects(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)
    subjects = user.subject_set.all()

    context = {
        "user_school_id": request.session.get("user_school_id"),
        "user_first_name": request.session.get("user_first_name"),
        "user_last_name": request.session.get("user_last_name"),
        "user_other_names": request.session.get("user_other_names"),
        # 'user_profile_pic': request.session.get('user_profile_pic'),
        "user": user,
        "subjects": subjects,
    }

    return render(request, "staff_templates/staff_subjects.html", context)


# def select_assessment_term(request, user_school_id, subject_id, assessment_action):
#     subject = Subject.objects.get(id=subject_id)
#     terms = Term.objects.all()
#     sessions = Session.objects.all()
#     if assessment_action == "staff_add_result":
#         staff_add_result = True
#         context = {
#         "user_school_id": user_school_id,
#         "user_first_name": request.session.get("user_first_name"),
#         "user_last_name": request.session.get("user_last_name"),
#         "user_other_names": request.session.get("user_other_names"),
#         "subject": subject,
#         "terms": terms,
#         "sessions": sessions,
#         "staff_add_result": staff_add_result
#         }

#         return render(request, "staff_templates/select_assessment_term.html", context)

#     if assessment_action == "staff_final_assessment":
#         staff_add_result = False
#         context = {
#         "user_school_id": user_school_id,
#         "user_first_name": request.session.get("user_first_name"),
#         "user_last_name": request.session.get("user_last_name"),
#         "user_other_names": request.session.get("user_other_names"),
#         "subject": subject,
#         "terms": terms,
#         "sessions": sessions,
#         "staff_add_result": staff_add_result
#         }
#         return render(request, "staff_templates/select_assessment_term.html", context)


def staff_add_result(request, user_school_id, subject_id):
    subject = Subject.objects.get(id=subject_id)
    sessions = Session.objects.all()
    students = subject.class_level.student_set.all()
    current_session = Session.objects.get(current_session=True)
    current_term = Term.objects.get(current_term=True)
    current_term_assessments = StudentAssessment.objects.filter(session=current_session, subject=subject)

    context = {
        "user_school_id": user_school_id,
        "user_first_name": request.session.get("user_first_name"),
        "user_last_name": request.session.get("user_last_name"),
        "user_other_names": request.session.get("user_other_names"),
        "subject": subject,
        "students": students,
        "assessment_choices": StudentAssessment.assessment_choices,
        "assessments": current_term_assessments,
        "sessions": sessions,
        "current_session": current_session,
        "current_term": current_term,
        "subject_term_id": str(subject.id) + "," + str(current_term.id),
    }

    return render(request, "staff_templates/staff_add_result.html", context)


def get_students_assessment(request, user_school_id):
    subject_id = request.GET.get("subjectId")
    session_id = request.GET.get("sessionId")
    current_session = Session.objects.get(current_session=True)
    subject = Subject.objects.get(id=subject_id)
    terms = Session.objects.get(id=session_id).term_set.all()

    if current_session.id == int(session_id):
        print('triggered')
        students = subject.class_level.student_set.all()
    else:
        students =  Student.objects.filter(studentassessment__session=session_id, studentassessment__subject=subject).distinct()

    data = {"terms": list(terms.values()), "students": []}

    for index, student in enumerate(list(students.values())):
        student_user = User.objects.get(student__id=student["id"])
        student_data = {
            "school_id": student_user.school_id,
            "first_name": student_user.first_name,
            "last_name": student_user.last_name,
            "other_name": student_user.other_names,
            "assessments": {},
        }
        for term in terms:
            student_data["assessments"][term.id] = list(
                student_user.student.studentassessment_set.filter(term=term).values()
            )
        data["students"].append(student_data)

    return JsonResponse(
        data,
        content_type="application/json",
        safe=False,
    )


def save_student_result(request, user_school_id):
    if request.method != "POST":
        print("failed")
        return redirect("/" + user_school_id + "/subjects")

    data = json.loads(request.POST["data"])
    subject = Subject.objects.get(id=data.get("subject_id"))
    session = Session.objects.get(id=data.get("session_id"))
    term = Term.objects.get(id=data.get("term_id"))
    deleted_assessments = data.get("deleted_assessments")
    new_assessments = data.get("new_assessments")
    edited_assessments = data.get("edited_assessments")
    msg = []
    try:
        with transaction.atomic():

            # handle deleted assessments
            if deleted_assessments:
                # for assessment in deleted_assessments:
                #     assessment_obj_list = StudentAssessment.objects.filter(
                #         assessment_desc=assessment
                #     ).delete()
                for assessment in deleted_assessments:
                    assessment_obj_list = StudentAssessment.objects.filter(
                        session=session,
                        term=term,
                        subject=subject,
                        assessment_desc=assessment
                    ).delete()
                msg.append("deleted")

            # handle new assessments
            if new_assessments:
                for assessment in new_assessments:
                    student = User.objects.get(
                        school_id=assessment.get("student_school_id")
                    ).student
                    assessment_type = assessment.get("assessment_type")
                    assessment_desc = assessment.get("assessment_desc")
                    score = float(assessment.get("assessment_score"))

                    StudentAssessment.objects.create(
                        student=student,
                        subject=subject,
                        term=term,
                        session=session,
                        assessment_type=assessment_type,
                        assessment_desc=assessment_desc,
                        score=score,
                    )
                msg.append("added")

            # handle edited assessments
            if edited_assessments:
                for assessment in edited_assessments:
                    assessment_obj = StudentAssessment.objects.get(
                        id=assessment.get("assessment_id")
                    )
                    assessment_obj.assessment_desc = assessment.get("assessment_desc")
                    assessment_obj.score = assessment.get("assessment_score")
                    assessment_obj.save()
                msg.append("edited")

        messages.success(
            request, "Assessments {} successfully".format(" and ".join(msg))
        )

    except Exception as e:
        print("error: ", e)
        messages.error(request, "Failed to add assessments")

    finally:
        return JsonResponse(
            json.dumps(
                {
                    "redirectUrl": "/"
                    + user_school_id
                    + "/"
                    + str(subject.id)
                    + "/staff_add_result"
                }
            ),
            content_type="application/json",
            safe=False,
        )


def final_assessment(request, user_school_id, subject_id):
    subject = Subject.objects.get(id=subject_id)
    assessments = StudentAssessment.objects.filter(subject=subject_id)
    students = subject.class_level.student_set.all()
    assessments_student_zero = students[0].studentassessment_set.all()

    assessments_type_and_num = {}
    assessments_desc = {}

    for assessment in assessments_student_zero:

        if assessment.assessment_type in assessments_type_and_num:
            assessments_type_and_num[assessment.assessment_type] += 1
            assessments_desc[assessment.assessment_type] = assessments_desc[
                assessment.assessment_type
            ] + [assessment.assessment_desc]

        else:
            assessments_type_and_num[assessment.assessment_type] = 1
            assessments_desc[assessment.assessment_type] = [assessment.assessment_desc]

    context = {
        "user_school_id": user_school_id,
        "user_first_name": request.session.get("user_first_name"),
        "user_last_name": request.session.get("user_last_name"),
        "user_other_names": request.session.get("user_other_names"),
        "subject": subject,
        "students": students,
        "assessments": assessments,
        "assessments_type_and_number": assessments_type_and_num,
        "assessments_desc": assessments_desc,
    }

    return render(request, "staff_templates/final_assessment.html", context)
