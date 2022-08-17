from django import forms 
from django.forms import Form
from accounts.models import ClassLevel, Session


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    other_names = forms.CharField(label="Other Names", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    phone_number = forms.CharField(label="Phone Number", max_length=13, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Classes
    try:
        class_levels = ClassLevel.objects.all()
        class_level_list = []
        for class_level in class_levels:
            single_course = (class_level.id, class_level.class_level_name)
            class_level_list.append(single_course)
    except:
        class_level_list = []
    
    #For Displaying Sessions
    try:
        sessions = Session.objects.all()
        session_list = []
        for session in sessions:
            single_session = (session.id, str(session.session_start)+" to "+str(session.session_end))
            session_list.append(single_session)
            
    except:
        session_list = []
    
    gender_list = (
        (1,'Female'),
        (2,'Male'),
    )
    
    class_level_id = forms.ChoiceField(label="Class", choices=class_level_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_id = forms.ChoiceField(label="Session", choices=session_list, widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))



class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    other_names = forms.CharField(label="Other Names", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    phone_number = forms.CharField(label="Phone Number", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Courses
    try:
        class_levels = ClassLevel.objects.all()
        class_level_list = []
        for class_level in class_levels:
            single_class_level = (class_level.id, class_level.class_level_name)
            class_level_list.append(single_class_level)
    except:
        class_level_list = []

    #For Displaying Session Years
    try:
        sessions = Session.objects.all()
        session_list = []
        for session in sessions:
            single_session = (session.id, str(session.session_start)+" to "+str(session.session_end))
            session_list.append(single_session)
            
    except:
        session_list = []

    
    gender_list = (
        (2,'Male'),
        (1,'Female')
    )
    
    class_level_id = forms.ChoiceField(label="Class", choices=class_level_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_id = forms.ChoiceField(label="Session", choices=session_list, widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))