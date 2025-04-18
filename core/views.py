from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Question, Answer
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    return render(request, 'core/home.html')

@login_required
def dashboard_view(request):
    user_questions = Question.objects.filter(user=request.user)
    user_answers = Answer.objects.filter(user=request.user)
    context = {
        'questions': user_questions,
        'answers': user_answers,
    }
    return render(request, 'dashboard.html', context)

def search_results(request):
    query = request.GET.get('q')
    # Search logic here (e.g., querying Q&A entries)
    return render(request, 'search_results.html', {'query': query})

def profile(request):
    return render(request, 'profile.html')

def settings(request):
    return render(request, 'settings.html')

def help(request):
    return render(request, 'help.html')

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'core/question_list.html', {'questions': questions})

@login_required
def question_detail(request, pk):
    question = Question.objects.get(pk=pk)
    answers = Answer.objects.filter(question=question)
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
            return redirect('question_detail', pk=question.pk)
    else:
        answer_form = AnswerForm()
    return render(request, 'core/question_detail.html', {'question': question, 'answers': answers, 'answer_form': answer_form})

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'core/ask_question.html', {'form': form})