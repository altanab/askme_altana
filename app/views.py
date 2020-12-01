from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from app.models import Profile, Question
from django.contrib.auth.models import User
from django.contrib import auth, messages
from app.forms import LoginForm, AskForm, AnswerForm, RegisterForm, SettingsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def hot_questions(request):
    questions = Question.objects.order_by_rating().all()
    questions_per_page = paginate(questions, request)
    return render(request, 'hot_questions.html', {
        'questions': questions_per_page,
    })


@login_required
def new_question(request):
    if request.method == 'GET':
        form = AskForm()
    elif request.method == 'POST':
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user.profile
            question.save()
            return redirect(reverse('question', kwargs={'qid': question.id}))
    return render(request, 'new_question.html', {
        'form': form,
    })


def login(request):
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                value_next = request.POST.get('next')
                if value_next is not None and value_next != '' and value_next != '/login/':
                    return redirect(value_next)
                else:
                    return redirect('/')
            else:
                messages.error(request, 'username or password is not correct')
    return render(request, 'login.html', {
        'form': form
    })

def logout(request):
    auth.logout(request)
    value_next = request.GET.get('next')
    if value_next is not None and value_next != '':
        return redirect(value_next)
    else:
        return redirect('/')


def signup(request):
    if request.method == 'GET':
        form = RegisterForm()
    elif request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.avatar = form.cleaned_data.get('avatar')
            user.profile.save()
            user = auth.authenticate(request, username=user.username, password=form.cleaned_data.get('password1'))
            auth.login(request, user)
            value_next = request.POST.get('next')
            if value_next is not None and value_next != '' and value_next != '/login/':
                return redirect(value_next)
            else:
                return redirect('/')
    return render(request, 'signup.html', {
        'form': form
    })


@login_required
def settings(request):
    if request.method == 'GET':
        form = SettingsForm(instance=request.user)
    elif request.method == 'POST':
        form = SettingsForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    return render(request, 'settings.html', {
        'form': form
    })


@login_required
def password(request):
    if request.method == 'GET':
        form = PasswordChangeForm(user=request.user)
    elif request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/settings/')
    return render(request, 'change_password.html', {
        'form': form
    })


def question(request, qid):
    question = Question.objects.select_related().get(id=qid)
    if request.method == 'GET':
        form = AnswerForm()
    elif request.method == 'POST':
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user.profile
            answer.question = question
            answer.save()
            form = AnswerForm()
    answers = question.answer_set.order_by('-rating').all()
    answers_per_page = paginate(answers, request)
    return render(request, 'question.html', {
        'question': question,
        'answers':answers_per_page,
        'form': form,
    })


def tag_questions(request, sometag):
    questions = Question.objects.filter_by_tag(sometag).all()
    questions_per_page = paginate(questions, request)
    return render(request, 'tag_questions.html', {
        'tag': sometag,
        'questions': questions_per_page,
    })


def index(request):
    questions = Question.objects.order_by_date().all()
    questions_per_page = paginate(questions, request)
    return render(request, 'index.html', {
        'questions': questions_per_page,
    })


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(1)
    return objects
