from django.contrib.auth.backends import ModelBackend
from .models import Student


class UseridBackend(ModelBackend):
    """
    Custom authentication backend that uses userid instead of username
    """
    def authenticate(self, request, userid=None, password=None, **kwargs):
        try:
            # Get user by userid
            user = Student.objects.get(userid=userid)
            # Check password
            if user.check_password(password):
                return user
        except Student.DoesNotExist:
            return None
        return None
    
    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None
