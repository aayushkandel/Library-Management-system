from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Book, BookIssue


class StudentRegistrationForm(UserCreationForm):
    """Form for registering new students"""
    userid = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'})
    )
    branch = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Branch'})
    )
    mobile = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'})
    )
    
    class Meta:
        model = Student
        fields = ['username', 'userid', 'password1', 'password2', 'email', 'branch', 'mobile']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


class BookForm(forms.ModelForm):
    """Form for adding/editing books"""
    class Meta:
        model = Book
        fields = ['subject', 'title', 'author', 'serial', 'quantity']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Book Title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author Name'}),
            'serial': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Serial Number'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity', 'min': '1'}),
        }


class BookIssueForm(forms.ModelForm):
    """Form for issuing books"""
    class Meta:
        model = BookIssue
        fields = ['stdid', 'serial', 'issue', 'exp']
        widgets = {
            'stdid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student ID', 'readonly': 'readonly'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Book Serial Number'}),
            'issue': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'exp': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class LoginForm(forms.Form):
    """Custom login form"""
    userid = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User ID'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
