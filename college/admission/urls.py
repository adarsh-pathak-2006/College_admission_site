"""
URL Configuration for admission app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Student pages
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('payment/', views.payment_view, name='payment'),
    path('payment-status/<int:payment_id>/', views.payment_status, name='payment_status'),
    
    # Admin pages
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-applications/', views.manage_applications, name='manage_applications'),
    path('update-application-status/<int:student_id>/', views.update_application_status, name='update_application_status'),
    path('manage-courses/', views.manage_courses, name='manage_courses'),
    path('edit-course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),
]