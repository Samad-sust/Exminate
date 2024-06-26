from typing import Any
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Custom Imports
from .models import Course, CourseHistory, CourseVerificationToken
from exam.models import Exam
from .forms import CourseEnrolmentForm

# Create your views here.

class CourseListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Course
    context_object_name = 'courses'
    template_name = "course/course-catalog.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        user = self.request.user
        user_course_history = CourseHistory.objects.filter(user=user)
        taken_courses = set(history.course_id for history in user_course_history)
        context['taken_courses'] = taken_courses
        
        print(taken_courses)
        return context

class CourseDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Course
    context_object_name = "course"
    template_name = "course/course-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exams'] = Exam.objects.filter(course=self.kwargs.get('pk'))
        return context

@login_required(login_url='login')
def courseEnrolmentView(request, courseID=None):
    
    if request.POST:
        form = CourseEnrolmentForm(request.POST)
        if form.is_valid():

            user = request.user
            course_code = form.cleaned_data['course_code']
            verification_token = form.cleaned_data['verification_token']

            if CourseVerificationToken.objects.filter(course__code=course_code, token_code = verification_token).exists():
                token = CourseVerificationToken.objects.get(course__code=course_code, token_code = verification_token)
                course = Course.objects.get(code=course_code)
                if  token.no_of_tokens >= 1 and \
                    token.valid_from <= timezone.now() and \
                    token.valid_to >= timezone.now() and \
                    token.is_active == True:

                    CourseHistory.objects.create(
                        course=course,
                        user = user,
                        veri_code_used=verification_token
                    )
                    # redirect to outcome page with a success message
                    messages.success(request, "Course enrolment successfull, please go to your dashboard")
                    return redirect('course-enrolment-outcome')
                else:
                    # Shows an error message if entered an invalid token code
                    messages.error(request, "Token is not valid")

            else:
                # Shows an error message if entered an invalid token/course code
                messages.error(request, "Course code or token is not valid!")
        else:
            pass
    
    else:
        initial_data = {'course_code' : courseID} if courseID else {}
        form = CourseEnrolmentForm(initial=initial_data)
    
    context = {
        'form' : form,
    }
    return render(request, template_name='course/course-enrolment.html', context=context)

@login_required(login_url='login')
def courseEnrolmentOutcome(request):

    return render(request, template_name='course/course-enrolment-outcome.html')