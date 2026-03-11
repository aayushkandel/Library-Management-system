from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Student, Book, BookIssue
from .forms import StudentRegistrationForm, BookForm, BookIssueForm, LoginForm


def home(request):
    """Home page view"""
    return render(request, 'library/home.html')


def user_login(request):
    """Login view for students and admin"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            password = form.cleaned_data['password']
            
            # Check for admin login
            if userid == 'admin' and password == 'admin':
                request.session['is_admin'] = True
                request.session['userid'] = 'admin'
                messages.success(request, 'Welcome Admin!')
                return redirect('admin_dashboard')
            
            # Check for student login
            try:
                # Authenticate using userid (our USERNAME_FIELD)
                user = authenticate(request, userid=userid, password=password)
                if user is not None:
                    login(request, user)
                    request.session['userid'] = userid
                    messages.success(request, f'Welcome {user.username}!')
                    return redirect('student_dashboard')
                else:
                    messages.error(request, 'Invalid credentials!')
            except Exception as e:
                messages.error(request, f'Login error: {str(e)}')
    else:
        form = LoginForm()
    
    return render(request, 'library/login.html', {'form': form})


def user_logout(request):
    """Logout view"""
    logout(request)
    request.session.flush()
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


# Admin Views
def admin_dashboard(request):
    """Admin dashboard"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Access denied!')
        return redirect('login')
    
    total_students = Student.objects.filter(is_admin=False).count()
    total_books = Book.objects.count()
    total_issued = BookIssue.objects.count()
    
    context = {
        'total_students': total_students,
        'total_books': total_books,
        'total_issued': total_issued,
    }
    return render(request, 'library/admin_dashboard.html', context)


def add_student(request):
    """Add new student"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Access denied!')
        return redirect('login')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.is_admin = False
            student.save()
            messages.success(request, f'Student {student.username} added successfully!')
            return redirect('view_students')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'library/add_student.html', {'form': form})


def view_students(request):
    """View all students"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Access denied!')
        return redirect('login')
    
    students = Student.objects.filter(is_admin=False)
    return render(request, 'library/view_students.html', {'students': students})


def delete_student(request, userid):
    """Delete a student"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Access denied!')
        return redirect('login')
    
    student = get_object_or_404(Student, userid=userid)
    if request.method == 'POST':
        student.delete()
        messages.success(request, f'Student {userid} deleted successfully!')
        return redirect('view_students')
    
    return render(request, 'library/delete_student.html', {'student': student})


def add_book(request):
    """Add new book (Admin or Student)"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            if request.session.get('is_admin'):
                return redirect('view_books')
            else:
                return redirect('student_dashboard')
    else:
        form = BookForm()
    
    return render(request, 'library/add_book.html', {'form': form})


def view_books(request):
    """View all books"""
    books = Book.objects.all()
    return render(request, 'library/view_books.html', {'books': books})


def delete_book(request, serial):
    """Delete a book"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Access denied!')
        return redirect('login')
    
    book = get_object_or_404(Book, serial=serial)
    if request.method == 'POST':
        book.delete()
        messages.success(request, f'Book {serial} deleted successfully!')
        return redirect('view_books')
    
    return render(request, 'library/delete_book.html', {'book': book})


# Student Views
@login_required
def student_dashboard(request):
    """Student dashboard"""
    userid = request.session.get('userid')
    issued_books = BookIssue.objects.filter(stdid=userid)
    
    context = {
        'issued_books': issued_books,
        'userid': userid,
    }
    return render(request, 'library/student_dashboard.html', context)


@login_required
def issue_book(request):
    """Issue a book to student"""
    userid = request.session.get('userid')
    
    if request.method == 'POST':
        form = BookIssueForm(request.POST)
        if form.is_valid():
            serial = form.cleaned_data['serial']
            
            # Check if book exists
            try:
                book = Book.objects.get(serial=serial)
            except Book.DoesNotExist:
                messages.error(request, 'Book not found!')
                return render(request, 'library/issue_book.html', {'form': form})
            
            # Check if book is available (quantity check)
            if book.available_count <= 0:
                messages.error(request, f'Book "{book.title}" is not available. All copies are currently issued!')
                return render(request, 'library/issue_book.html', {'form': form})
            
            # Issue the book
            book_issue = form.save(commit=False)
            book_issue.stdid = userid
            book_issue.save()
            messages.success(request, f'Book "{book.title}" issued successfully! Available copies: {book.available_count}')
            return redirect('student_dashboard')
    else:
        # Get book serial from query parameter if provided
        book_serial = request.GET.get('book_serial', '')
        
        # Pre-fill student ID and book serial
        form = BookIssueForm(initial={
            'stdid': userid,
            'serial': book_serial,
            'issue': datetime.now().date(),
            'exp': (datetime.now() + timedelta(days=14)).date()
        })
    
    return render(request, 'library/issue_book.html', {'form': form})


@login_required
def return_book(request):
    """Return a book"""
    userid = request.session.get('userid')
    
    if request.method == 'POST':
        serial = request.POST.get('serial')
        try:
            book_issue = BookIssue.objects.filter(stdid=userid, serial=serial).first()
            book = Book.objects.get(serial=serial)
            book_issue.delete()
            messages.success(request, f'Book "{book.title}" returned successfully!')
            return redirect('student_dashboard')
        except BookIssue.DoesNotExist:
            messages.error(request, 'Book issue record not found!')
        except Book.DoesNotExist:
            messages.error(request, 'Book not found!')
    
    issued_books = BookIssue.objects.filter(stdid=userid)
    return render(request, 'library/return_book.html', {'issued_books': issued_books})


@login_required
def my_books(request):
    """View books issued to logged-in student"""
    userid = request.session.get('userid')
    issued_books = BookIssue.objects.filter(stdid=userid).select_related()
    
    # Get book details for each issued book
    books_data = []
    for issue in issued_books:
        try:
            book = Book.objects.get(serial=issue.serial)
            books_data.append({
                'issue': issue,
                'book': book
            })
        except Book.DoesNotExist:
            books_data.append({
                'issue': issue,
                'book': None
            })
    
    return render(request, 'library/my_books.html', {'books_data': books_data})


def view_issued_books(request):
    """View all issued books with student and book details (Admin only)"""
    if not request.session.get('is_admin'):
        messages.error(request, 'Access denied!')
        return redirect('login')
    
    # Get all issued books
    issued_books = BookIssue.objects.all().order_by('-issue')
    
    # Prepare data with book and student details
    issued_data = []
    for issue in issued_books:
        try:
            book = Book.objects.get(serial=int(issue.serial))
        except (Book.DoesNotExist, ValueError):
            book = None
        
        try:
            student = Student.objects.get(userid=issue.stdid)
        except Student.DoesNotExist:
            student = None
        
        issued_data.append({
            'issue': issue,
            'book': book,
            'student': student
        })
    
    return render(request, 'library/view_issued_books.html', {'issued_data': issued_data})
