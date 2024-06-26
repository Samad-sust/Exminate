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
from django.urls import path, re_path
from . import views

urlpatterns = [

    path('course-catalog/', views.CourseListView.as_view(), name="course-catalog"),
    path('detail/<int:pk>', views.CourseDetailView.as_view(), name="course-detail"),
    re_path(r'^enrolment/(?P<courseID>[^/]+)?/?$', views.courseEnrolmentView, name="course-enrolment"),
    path('enrolment-outcome/', views.courseEnrolmentOutcome, name="course-enrolment-outcome"),
    
]