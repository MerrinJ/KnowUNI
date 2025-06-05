"""education_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from education_app.views import *
from education_app import views###################

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', front_page, name='front_page'),
    path('front_page/', front_page, name='front_page'),
    path('about_page/', about_page, name='about_page'),
    path('contact_page/', contact_page, name='contact_page'),
    path('login_page/', login_page, name='login_page'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('home_page/', home_page, name='home_page'),
    path('course_rec/', course_rec, name='course_rec'),
    path('course/', course, name='course'),
    path('booking/', booking, name='booking'),
    path('course_recommendation_view/', course_recommendation_view, name='course_recommendation_view'),
    path('find_courses_view/', find_courses_view, name='find_courses_view'),
    path('find_prerequisites_view/', find_prerequisites_view, name='find_prerequisites_view'),
    path('prerequest/', prerequest, name='prerequest'),
    path("profile/", profile, name="profile_page"),
    path("logout/", logout, name="logout"),


]
