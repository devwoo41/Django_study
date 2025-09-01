from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
from .forms import QuestionForm

def index(request):
    question_list=Question.objects.order_by('-create_date')
    context = {'question_list':question_list}
    return render(request, 'pybo/question_list.html',context)

def detail(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    context={'question':question}
    return render(request,'pybo/question_detall.html',context)

def answer_create(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    question.answer_set.create(content=request.POST.get('content'),create_date=timezone.now())
    return redirect('pybo:detail',question_id=question.id)

def question_create(request):
    if request.method=='POST':
        form=QuestionForm(request.POST)
        if form.is_valid():
            question=form.save(commit=False)
            question.create_date=timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form=QuestionForm()
    context={'form':form}
    return render(request, 'pybo/question_form.html',context)
# answer_create 함수의 매개변수 question_id는 url 매핑에 의해 값이 전달된다. 예를 들어, http://127.0.0.1:8000/pybo/answer/create/2
# 페이지를 요청하면 question_id 매개변수에 2라는 값이 전달된다.
# 그리고 답변을 등록할 때 텍스트창에 입력한 내용은 answer_create 함수의 첫번째 매개변수인 request 객체를 통해 읽을 수 있다.