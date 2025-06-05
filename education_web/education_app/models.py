from django.db import models

class Student(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define the ID field
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    qualification = models.CharField(max_length=200)  # Highest qualification
    interest_areas = models.TextField()  # Areas of interest
    password = models.CharField(max_length=255)  # Store hashed password for security

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    courses = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="resumes/")
    skills = models.TextField()
    interests = models.TextField()
    courses = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Course(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    skill = models.CharField(max_length=255)
    university = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.name  # This shows the course name
    




