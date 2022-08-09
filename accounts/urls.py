from django.urls import path

from . import views
from . import views_admin

urlpatterns = [
    path('', views.login_page, name="login_page"),
    path('doLogin', views.do_login, name="do_login"),
    path('admin/', views_admin.home, name="admin_home"),
    path('admin/profile/', views_admin.profile, name="admin_profile"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin/manage_student', views_admin.manage_student, name="manage_student"),
    path('admin/manage_staff', views_admin.manage_staff, name="manage_staff"),
    path('admin/manage_class', views_admin.manage_class, name="manage_class"),
    path('admin/manage_subject', views_admin.manage_subject, name="manage_subject"),
]
