from django.core.management.base import BaseCommand
from library.models import Student


class Command(BaseCommand):
    help = 'Creates a test student account'

    def handle(self, *args, **kwargs):
        # Check if student already exists
        if Student.objects.filter(userid='student1').exists():
            self.stdout.write(self.style.WARNING('Student "student1" already exists!'))
            student = Student.objects.get(userid='student1')
            # Update password
            student.set_password('12345')
            student.save()
            self.stdout.write(self.style.SUCCESS('Password updated for student1'))
        else:
            # Create new student
            student = Student.objects.create_user(
                userid='student1',
                username='Test Student',
                password='12345',
                email='student1@example.com',
                branch='Computer Science',
                mobile='9334788154'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created student account!'))
        
        self.stdout.write(self.style.SUCCESS('\n=== Test Student Credentials ==='))
        self.stdout.write(self.style.SUCCESS('User ID: student1'))
        self.stdout.write(self.style.SUCCESS('Password: 12345'))
        self.stdout.write(self.style.SUCCESS('================================\n'))
