from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Question, Answer
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from .models import Answer, Vote
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Sum

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

@csrf_exempt
def vote_answer(request, answer_id, vote_type):
    if request.method == 'POST':
        try:
            # Get the vote value (1 for upvote, -1 for downvote)
            vote_value = 1 if vote_type == 'up' else -1

            # Assuming the user is logged in and there is an Answer object
            answer = Answer.objects.get(id=answer_id)
            vote, created = Vote.objects.get_or_create(
                user=request.user,
                answer=answer,
                defaults={'value': vote_value}  # Set the vote value on creation
            )

            if not created:
                # If the vote already exists, update the value
                vote.value = vote_value
                vote.save()

            # Return the new vote count for the answer
            vote_count = Vote.objects.filter(answer=answer).aggregate(Sum('value'))['value__sum'] or 0

            return JsonResponse({'success': True, 'vote_count': vote_count})

        except Answer.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Answer not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

 

@csrf_exempt  # or use @login_required + handle csrf in frontend
@login_required
def vote_answer_ajax(request, answer_id, vote_type):
    if request.method == 'POST':
        try:
            answer = Answer.objects.get(pk=answer_id)
            vote_value = 1 if vote_type == 'up' else -1

            vote, created = Vote.objects.get_or_create(user=request.user, answer=answer)
            vote.value = vote_value
            vote.save()

            vote_count = answer.vote_count()
            return JsonResponse({'success': True, 'vote_count': vote_count})
        except Answer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Answer not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})