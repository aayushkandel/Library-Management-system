from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class StudentManager(BaseUserManager):
    """Manager for Student model"""
    def create_user(self, userid, password=None, **extra_fields):
        if not userid:
            raise ValueError('User must have a userid')
        user = self.model(userid=userid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, userid, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(userid, password, **extra_fields)


class Student(AbstractBaseUser, PermissionsMixin):
    """Custom user model for students"""
    username = models.CharField(max_length=50, verbose_name='name')
    userid = models.CharField(max_length=20, primary_key=True)
    email = models.EmailField(blank=True)
    branch = models.CharField(max_length=30, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = StudentManager()
    
    USERNAME_FIELD = 'userid'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'Login'
    
    def __str__(self):
        return f"{self.username} ({self.userid})"


class Book(models.Model):
    """Model for books in the library"""
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    serial = models.IntegerField(primary_key=True)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'Book'
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    @property
    def available_count(self):
        """Calculate available copies of the book"""
        issued_count = BookIssue.objects.filter(serial=str(self.serial)).count()
        return self.quantity - issued_count


class BookIssue(models.Model):
    """Model for tracking issued books"""
    stdid = models.CharField(max_length=20)
    serial = models.CharField(max_length=10)
    issue = models.DateField()
    exp = models.DateField()
    
    class Meta:
        db_table = 'BookIssue'
    
    def __str__(self):
        return f"Book {self.serial} issued to {self.stdid}"
