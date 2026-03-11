from django.urls import path
from . import views

urlpatterns = [
    # Home and Auth
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-student/', views.add_student, name='add_student'),
    path('view-students/', views.view_students, name='view_students'),
    path('delete-student/<str:userid>/', views.delete_student, name='delete_student'),
    
    # Book Management (Admin/Student)
    path('add-book/', views.add_book, name='add_book'),
    path('view-books/', views.view_books, name='view_books'),
    path('delete-book/<int:serial>/', views.delete_book, name='delete_book'),
    path('view-issued-books/', views.view_issued_books, name='view_issued_books'),
    
    # Student URLs
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('issue-book/', views.issue_book, name='issue_book'),
    path('return-book/', views.return_book, name='return_book'),
    path('my-books/', views.my_books, name='my_books'),
]
