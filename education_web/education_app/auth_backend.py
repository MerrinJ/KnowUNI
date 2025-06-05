from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from education_app.models import Student  # replace with your actual app name

class StudentBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            student = Student.objects.get(email=username)
            if student.password == password:
                user, created = User.objects.get_or_create(username=student.email)
                return user
        except Student.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
