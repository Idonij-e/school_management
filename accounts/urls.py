from django.urls import path

from . import views
from . import views_admin

urlpatterns = [
    path('', views.login_page, name="login_page"),
    path('doLogin', views.do_login, name="do_login"),
    # path('admin/', views_admin.home, name="admin_home"),
    path('<user_school_id>', views_admin.home, name="admin_home"),
    path('<user_school_id>/profile', views_admin.profile, name="admin_profile"),
    path('logout_user/', views.logout_user, name="logout_user"),

    path('<user_school_id>/add_staff', views_admin.add_staff, name="add_staff"),
    path('<user_school_id>/add_student', views_admin.add_student, name="add_student"),
    path('<user_school_id>/add_class', views_admin.add_class, name="add_class"),
    path('<user_school_id>/add_subject', views_admin.add_subject, name="add_subject"),
    path('<user_school_id>/add_session', views_admin.add_session, name="add_session"),

    path('<user_school_id>/add_staff_save', views_admin.add_staff_save, name="add_staff_save"),
    path('<user_school_id>/add_class_save', views_admin.add_class_save, name="add_class_save"),
    path('<user_school_id>/add_subject_save', views_admin.add_subject_save, name="add_subject_save"),
    path('<user_school_id>/add_session_save', views_admin.add_session_save, name="add_session_save"),

    path('<user_school_id>/edit_staff/<staff_id>', views_admin.edit_staff, name="edit_staff"),
    path('<user_school_id>/edit_student/<student_id>', views_admin.edit_student, name="edit_student"),
    path('<user_school_id>/edit_class/<class_id>', views_admin.edit_class, name="edit_class"),
    path('<user_school_id>/edit_subject/<subject_id>', views_admin.edit_subject, name="edit_subject"),
    path('<user_school_id>/edit_session/<session_id>', views_admin.edit_subject, name="edit_session"),

    path('<user_school_id>/delete_staff/<staff_id>', views_admin.delete_staff, name="delete_staff"),
    path('<user_school_id>/delete_student/<student_id>', views_admin.delete_student, name="delete_student"),
    path('<user_school_id>/delete_class/<class_id>', views_admin.delete_class, name="delete_class"),
    path('<user_school_id>/delete_subject/<subject_id>', views_admin.delete_subject, name="delete_subject"),    
    path('<user_school_id>/delete_session/<session_id>', views_admin.delete_session, name="delete_session"),    

    path('<user_school_id>/manage_staff', views_admin.manage_staff, name="manage_staff"),
    path('<user_school_id>/manage_students', views_admin.manage_students, name="manage_students"),
    path('<user_school_id>/manage_class', views_admin.manage_class, name="manage_class"),
    path('<user_school_id>/manage_subject', views_admin.manage_subject, name="manage_subject"),
    path('<user_school_id>/manage_session', views_admin.manage_session, name="manage_session"),
]
