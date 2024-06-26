"""
URL configuration for Exminate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('dashboard/', views.student_dashboard, name="st_dashboard"),
    path('teacher_dashboard/', views.teacher_dashboard, name="te_dashboard"), # we won't need this in future, keeping this untill then
    path('login/', views.examinatelogin, name="login"),
    path('signup/',views.examinatesignup, name="sign_up")
]