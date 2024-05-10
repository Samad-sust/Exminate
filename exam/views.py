from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

# custom imports 
from .models import Exam
from question.models import MCQ, ShortQues, LongQues
from .custom_func import process_mcq_and_shortQ, process_longQ
# Create your views here.
class ExamListView(ListView):
    model = Exam
    context_object_name = 'exams'
    template_name = "exam/exams.html"

class ExamDetailView(DetailView):
    model = Exam
    context_object_name = 'exam'
    template_name = "exam/exam-detail.html"

class ExamQuestionDetailView(DetailView):
    model = Exam
    context_object_name = 'exam'
    template_name = "exam/exam-questions.html"

    def get(self, request, *args, **kwargs):
        # Get the exam object
        self.object = self.get_object()
        # Store exam ID in session
        request.session['exam_id'] = self.object.pk
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mcqs'] = MCQ.objects.filter(exam=self.kwargs.get('pk'))
        context['shortQues'] = ShortQues.objects.filter(exam=self.kwargs.get('pk'))
        context['longQues'] = LongQues.objects.filter(exam=self.kwargs.get('pk'))
        return context

def ExamCompleteView(request):
    """View for ExamComplete Page"""
    question_type = {'mcq' : 1, 'shortQ': 2, 'longQ': 3, 'code': 4}

    if request.method == "POST":
        exam_id = request.session.get('exam_id')
        user_id = request.user.pk

        mcq_answers = {}
        shortQ_answers = {}
        longQ_answers = {}

        mcq_score, shortQScore, longQ_score = (0,0,0)
        # Seperate answers according to the questions
        for k, v in request.POST.items():
            v = v.strip() # stripping whitespaces from the user inputs

            if k.startswith("mcq_"):
                mcq_answers[k] = v
            elif k.startswith("sq_"):
                if v != "":
                    shortQ_answers[k] = v
            elif k.startswith("lq_"):
                if v != "":
                    longQ_answers[k] =  v
        
        if mcq_answers:
            mcq_score = process_mcq_and_shortQ(user_id=user_id, exam_id=exam_id, ques_type=question_type['mcq'], answer_dict=mcq_answers)
        if shortQ_answers:
            shortQ_score = process_mcq_and_shortQ(user_id=user_id, exam_id=exam_id, ques_type=question_type['shortQ'], answer_dict=shortQ_answers)
        if longQ_answers:
            longQ_score = process_longQ(user_id=user_id, exam_id=exam_id, ques_type=question_type['longQ'], answer_dict=longQ_answers)

        print('MCQ', mcq_score, 'Short Q', shortQ_score, "LongQ", longQ_score)
 
    return render(request, 'exam/exam-complete.html')