import email
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.models import User, Administrator, Staff, Student, Session, ClassLevel, Subject
from accounts.forms import AddStudentForm, EditStudentForm
from accounts.utils import generate_school_id

def home(request, **kwargs):

    user = User.objects.get(school_id=kwargs.get('user_school_id'))

    all_student_count = Student.objects.all().count()
    subject_count = Subject.objects.all().count()
    class_level_count = ClassLevel.objects.all().count()
    staff_count = Staff.objects.all().count()

    # Total Subjects and students in Each Course
    class_level_all = ClassLevel.objects.all()
    class_level_name_list = []
    subject_count_list = []
    student_count_list_in_class_level = []

    for class_level in class_level_all:
        subjects = Subject.objects.filter(class_level_id=class_level.id).count()
        students = Student.objects.filter(class_level_id=class_level.id).count()
        class_level_name_list.append(class_level.class_level_name)
        subject_count_list.append(subjects)
        student_count_list_in_class_level.append(students)
    
    subject_all = Subject.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subject_all:
        class_level = ClassLevel.objects.get(id=subject.class_level.id)
        student_count = Student.objects.filter(class_level_id=class_level.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)
    
    # For Saffs
    staff_name_list=[]

    staffs = Staff.objects.all()
    for staff in staffs:
        staff_name_list.append(staff.user.first_name)

    # For Students
    student_name_list=[]

    students = Student.objects.all()
    for student in students:
        student_name_list.append(student.user.first_name)


    context={
        'user': user,
        "all_student_count": all_student_count,
        "subject_count": subject_count,
        "class_level_count": class_level_count,
        "staff_count": staff_count,
        "class_level_name_list": class_level_name_list,
        "subject_count_list": subject_count_list,
        "student_count_list_in_class_level": student_count_list_in_class_level,
        "subject_list": subject_list,
        "student_count_list_in_subject": student_count_list_in_subject,
        "staff_name_list": staff_name_list,
        "student_name_list": student_name_list,
    }

    return render(request, 'admin_templates/home.html', context)


# Administrator profile

def profile(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)

    context={
        "user": user
    }
    return render(request, 'admin_templates/admin_profile.html', context)

def edit_admin_profile(request, user_school_id):

    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("/" + user_school_id + 'profile')

    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        other_names = request.POST.get('other_names')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        school_id = request.POST.get('school_id')

        try:
            user = User.objects.get(school_id=school_id)
            user.first_name = first_name
            user.last_name = last_name
            user.other_names = other_names
            user.email = email
            user.phone_number = phone_number

            if password != None and password != "":
                user.set_password(password)
                
            user.save()
            messages.success(request, "Profile Updated Successfully")
            
        except:
            messages.error(request, "Failed to Update Profile")

        finally:
            return redirect("/" + user_school_id + 'profile')    

# STAFF

def manage_staff(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)
    staff_list = Staff.objects.all()
    context = { 
        "user": user,
        "staff_list": staff_list
        }

    return render(request, 'admin_templates/manage_staff_template.html', context)

def add_staff(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)
    context = {
        "user": user
    }
    return render(request, "admin_templates/add_staff_template.html", context)

def add_staff_save(request, user_school_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect("/" + user_school_id + '/add_staff')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        other_names = request.POST.get('other_names')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        username = generate_school_id()

        try:
            user = User.objects.create_user(
                username=username, 
                password=password, 
                email=email, 
                first_name=first_name, 
                last_name=last_name, 
                other_names=other_names,
                phone_number=phone_number,
                user_type=2)


            messages.success(request, "Staff Added Successfully!")

        except:
            messages.error(request, "Failed to Add Staff!")

        finally:
            return redirect("/" + user_school_id + '/add_staff')

def edit_staff(request, user_school_id, staff_school_id):
    user = User.objects.get(school_id=user_school_id)

    staff = User.objects.get(school_id=staff_school_id).staff
    context = {
        "user": user,
        "staff": staff
    }
    return render(request, "admin_templates/edit_staff_template.html", context)

def edit_staff_save(request, user_school_id):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_school_id = request.POST.get('staff_school_id')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        other_names = request.POST.get('other_names')
        phone_number = request.POST.get('phone_number')

        try:
            # INSERTING into User Model
            user = User.objects.get(school_id=staff_school_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.other_names = other_names
            user.phone_number = phone_number
            user.save()

            messages.success(request, "Staff Updated Successfully.")

        except:
            messages.error(request, "Failed to Update Staff.")

        finally:
            return redirect("/" + user_school_id + '/edit_staff/' + staff_school_id)

def delete_staff(request, user_school_id, staff_school_id):
    staff = User.objects.get(school_id=staff_school_id)
    
    try: 
        staff.delete()
        messages.success(request, "Staff Deleted Successfully.")

    except:
        messages.error(request, "Failed to Delete Staff.")
        
    finally:
        return redirect("/" + user_school_id + "/manage_staff")


# STUDENTS

def manage_students(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)

    students = Student.objects.all()
    context = {
        "user": user,
        "students": students
    }
    return render(request, 'admin_templates/manage_students_template.html', context)

def add_student(request, user_school_id):
    form = AddStudentForm()
    context = {
        "user_school_id": user_school_id,
        "form": form
    }
    return render(request, 'admin_templates/add_student_template.html', context)

def add_student_save(request, user_school_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("/" + user_school_id + '/add_student')
    else:
        form = AddStudentForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            other_names = form.cleaned_data['other_names']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            session_id = form.cleaned_data['session_id']
            class_level_id = form.cleaned_data['class_level_id']
            gender = form.cleaned_data['gender']
            username = generate_school_id()

            

    #         # Getting Profile Pic first
    #         # First Check whether the file is selected or not
    #         # Upload only if file is selected
    #         # if len(request.FILES) != 0:
    #         #     profile_pic = request.FILES['profile_pic']
    #         #     fs = FileSystemStorage()
    #         #     filename = fs.save(profile_pic.name, profile_pic)
    #         #     profile_pic_url = fs.url(filename)
    #         # else:
    #         #     profile_pic_url = None
    #         profile_pic_url = ""

            try:
                user = User.objects.create_user(username=username, 
                password=password, 
                email=email, 
                first_name=first_name, 
                last_name=last_name, 
                other_names=other_names,
                user_type=3,
                phone_number=phone_number,
                gender=gender)

                user.student.address = address
                user.student.phone_number = phone_number

                class_level = ClassLevel.objects.get(id=class_level_id)
                user.student.class_level = class_level

                session = Session.objects.get(id=session_id)
                user.student.session = session

                user.save()

                messages.success(request, "Student Added Successfully!")

            except:
                messages.error(request, "Failed to Add Student!")
            
            finally: 
                return redirect("/" + user_school_id + '/add_student')

        else:
            return redirect("/" + user_school_id + '/add_student')

def edit_student(request, user_school_id, student_school_id):
    # Adding Student ID into Session Variable
    request.session['student_school_id'] = student_school_id

    student_user = User.objects.get(school_id=student_school_id)
    form = EditStudentForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = student_user.email
    form.fields['first_name'].initial = student_user.first_name
    form.fields['last_name'].initial = student_user.last_name
    form.fields['other_names'].initial = student_user.other_names
    form.fields['address'].initial = student_user.student.address
    form.fields['class_level_id'].initial = student_user.student.class_level.id
    form.fields['gender'].initial = student_user.gender
    form.fields['session_id'].initial = student_user.student.session.id
    form.fields['phone_number'].initial = student_user.phone_number

    context = {
        "user_school_id": user_school_id,
        "student": student_user,
        "form": form
    }
    return render(request, "admin_templates/edit_student_template.html", context)

def edit_student_save(request, user_school_id):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_school_id = request.session.get('student_school_id')

        if student_school_id == None:
            return redirect("/" + user_school_id + '/manage_student')

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            other_names = form.cleaned_data['other_names']
            address = form.cleaned_data['address']
            class_level_id = form.cleaned_data['class_level_id']
            gender = form.cleaned_data['gender']
            session_id = form.cleaned_data['session_id']
            phone_number = form.cleaned_data['phone_number']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            # if len(request.FILES) != 0:
            #     profile_pic = request.FILES['profile_pic']
            #     fs = FileSystemStorage()
            #     filename = fs.save(profile_pic.name, profile_pic)
            #     profile_pic_url = fs.url(filename)
            # else:
            #     profile_pic_url = None

            try:
                # First Update into User Model
                user = User.objects.get(school_id=student_school_id)
                user.first_name = first_name
                user.last_name = last_name
                user.other_names = other_names
                user.email = email
                user.phone_number = phone_number
                user.gender = gender
                user.save()

                # Then Update Students Table
                student_model = user.student
                student_model.address = address

                class_level = ClassLevel.objects.get(id=class_level_id)
                student_model.class_level = class_level

                session = Session.objects.get(id=session_id)
                student_model.session = session

                # if profile_pic_url != None:
                #     student_model.profile_pic = profile_pic_url

                student_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['student_school_id']

                messages.success(request, "Student Updated Successfully!")

            except:
                messages.success(request, "Failed to Uupdate Student.")

            finally:
                return redirect("/" + user_school_id + '/edit_student/' + student_school_id)

        else:
            return redirect("/" + user_school_id + '/edit_student/' + student_school_id)

def delete_student(request, user_school_id, student_school_id):
    student = User.objects.get(school_id=student_school_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")

    except:
        messages.error(request, "Failed to Delete Student.")

    finally:
        return redirect("/" + user_school_id + '/manage_students')

# CLASSES

def manage_class(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)

    class_levels = ClassLevel.objects.all()
    context = {
        "user": user,
        "class_levels": class_levels
    }
    return render(request, 'admin_templates/manage_class_template.html', context)

def add_class(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)

    context = {
        "user": user
    }
    return render(request, "admin_templates/add_class_template.html", context)

def add_class_save(request, user_school_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("/" + user_school_id +  '/add_class')

    else:
        class_level_name = request.POST.get('class_level_name')
        try:
            course_model = ClassLevel(class_level_name=class_level_name)
            course_model.save()
            messages.success(request, "Class Added Successfully!")

        except:
            messages.error(request, "Failed to Add Class!")

        finally:
            return redirect("/" + user_school_id +  '/add_class')

def edit_class(request, user_school_id, class_level_id):
    class_level = ClassLevel.objects.get(id=class_level_id)
    context = {
        "user_school_id": user_school_id,
        "class_level": class_level,
    }
    return render(request, 'admin_templates/edit_class_template.html', context)

def edit_class_save(request, user_school_id):
    if request.method != "POST":
        HttpResponse("Invalid Method")

    else:
        class_level_id = request.POST.get('class_level_id')
        class_level_name = request.POST.get('class_level_name')

        try:
            class_level = ClassLevel.objects.get(id=class_level_id)
            class_level.class_level_name = class_level_name
            class_level.save()

            messages.success(request, "Class Updated Successfully.")

        except:
            messages.error(request, "Failed to Update Class.")

        finally:
            return redirect("/" + user_school_id + '/edit_class/' + class_level_id)

def delete_class(request, user_school_id, class_level_id):
    class_level = ClassLevel.objects.get(id=class_level_id)
    try:
        class_level.delete()
        messages.success(request, "Class Deleted Successfully.")

    except:
        messages.error(request, "Failed to Delete class.")

    finally:
        return redirect("/" + user_school_id + '/manage_class')


# SUBJECTS


def manage_subject(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)

    subjects = Subject.objects.all()
    context = {
        "user": user,
        "subjects": subjects
    }
    return render(request, 'admin_templates/manage_subject_template.html', context)

def add_subject(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)

    class_levels = ClassLevel.objects.all()
    staff_list = User.objects.filter(user_type='2')
    context = {
        "user": user,
        "class_levels": class_levels,
        "staff_list": staff_list
    }
    return render(request, 'admin_templates/add_subject_template.html', context)

def add_subject_save(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)

    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect("/" + user_school_id + '/add_subject')
    else:
        subject_name = request.POST.get('subject')
        class_level_id = request.POST.get('class')
        class_level = ClassLevel.objects.get(id=class_level_id)
        
        staff_id = request.POST.get('staff')
        staff = User.objects.get(id=staff_id)

        try:
            subject = Subject(subject_name=subject_name, class_level=class_level, staff=staff)
            subject.save()
            messages.success(request, "Subject Added Successfully!")

        except:
            messages.error(request, "Failed to Add Subject!")

        finally:
            return redirect("/" + user_school_id + '/add_subject')

def edit_subject(request, user_school_id, subject_id):
    subject = Subject.objects.get(id=subject_id)
    class_levels = ClassLevel.objects.all()
    staff_list = User.objects.filter(user_type='2')
    context = {
        "user_school_id": user_school_id,
        "subject": subject,
        "class_levels": class_levels,
        "staff_list": staff_list,
    }
    return render(request, 'admin_templates/edit_subject_template.html', context)

def edit_subject_save(request, user_school_id):
    if request.method != "POST":
        HttpResponse("Invalid Method.")

    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        class_level_id = request.POST.get('class_level_id')
        staff_id = request.POST.get('staff_id')

        try:
            subject = Subject.objects.get(id=subject_id)
            subject.subject_name = subject_name

            class_level = ClassLevel.objects.get(id=class_level_id)
            subject.class_level = class_level

            staff = User.objects.get(id=staff_id)
            subject.staff = staff
            
            subject.save()

            messages.success(request, "Subject Updated Successfully.")
            # return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))

        except:
            messages.error(request, "Failed to Update Subject.")
            # return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))

        finally:
            return redirect("/" + user_school_id + '/edit_subject/' + subject_id)

def delete_subject(request, user_school_id, subject_id):
    subject = Subject.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")

    except:
        messages.error(request, "Failed to Delete Subject.")

    finally:
        return redirect("/" + user_school_id + '/manage_subject')

# SESSION

def manage_session(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)

    sessions = Session.objects.all()
    context = {
        "user": user,
        "sessions": sessions
    }
    return render(request, "admin_templates/manage_session_template.html", context)

def add_session(request, user_school_id):
    user = User.objects.get(school_id=user_school_id)

    context = {
        "user": user
    }
    return render(request, "admin_templates/add_session_template.html", context)

def add_session_save(request, user_school_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("/" + user_school_id + '/manage_session')

    else:
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')

        try:
            session = Session(session_start=session_start, session_end=session_end)
            session.save()
            messages.success(request, "Session added Successfully!")

        except:
            messages.error(request, "Failed to Add Session")

        finally:
            return redirect("/" + user_school_id + '/manage_session')

def edit_session(request, user_school_id, session_id):
    session = Session.objects.get(id=session_id)
    context = {
        "user_school_id": user_school_id,
        "session": session
    }
    return render(request, "admin_templates/edit_session_template.html", context)

def edit_session_save(request, user_school_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect("/" + user_school_id + '/manage_session')

    else:
        session_id = request.POST.get('session_id')
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')

        try:
            session_year = Session.objects.get(id=session_id)
            session_year.session_start = session_start
            session_year.session_end = session_end
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")

        except:
            messages.error(request, "Failed to Update Session.")

        finally:
            return redirect("/" + user_school_id + '/manage_session')

def delete_session(request,user_school_id, session_id):
    session = Session.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")

    except:
        messages.error(request, "Failed to Delete Session.")
    
    finally:
        return redirect("/" + user_school_id + '/manage_session')
