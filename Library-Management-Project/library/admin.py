from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Book, BookIssue


@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ['username', 'userid', 'email', 'branch', 'mobile', 'is_admin']
    list_filter = ['is_admin', 'branch']
    search_fields = ['username', 'userid', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('userid', 'branch', 'mobile', 'is_admin')}),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['serial', 'title', 'author', 'subject']
    list_filter = ['subject', 'author']
    search_fields = ['title', 'author', 'serial']


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['stdid', 'serial', 'issue', 'exp']
    list_filter = ['issue', 'exp']
    search_fields = ['stdid', 'serial']
    date_hierarchy = 'issue'
