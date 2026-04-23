from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('lessons/', views.lessons, name='lessons'),
    path('course/<int:course_id>/', views.course, name='course'),
    path('complete/<int:lesson_id>/', views.complete_lesson, name='complete_lesson'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('reset/<int:course_id>/', views.reset_progress, name='reset_progress'),

    path('admin-login/', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/courses/', views.admin_courses, name='admin_courses'),
    path('dashboard/courses/add/', views.admin_add_course, name='admin_add_course'),
    path('dashboard/courses/edit/<int:id>/', views.admin_edit_course, name='admin_edit_course'),
    path('dashboard/courses/delete/<int:id>/', views.admin_delete_course, name='admin_delete_course'),

    path('dashboard/lessons/', views.admin_lessons, name='admin_lessons'),
    path('dashboard/lessons/add/<int:course_id>/', views.admin_add_lesson, name='admin_add_lesson'),
    path('dashboard/lessons/edit/<int:id>/', views.admin_edit_lesson, name='admin_edit_lesson'),
    path('dashboard/lessons/delete/<int:id>/', views.admin_delete_lesson, name='admin_delete_lesson'),
    path('dashboard/lessons/<int:course_id>/', views.admin_course_lessons, name='admin_course_lessons'),

    path('dashboard/content/add/<int:lesson_id>/', views.admin_add_content, name='admin_add_content'),

    path('dashboard/users/', views.admin_users, name='admin_users'),
]