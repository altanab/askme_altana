from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from app.models import Profile, Question, Answer
from django.contrib.auth.models import User
from django.db.models import Count, Sum


def hot_questions(request):
    questions = Question.objects.order_by_rating().all()
    questions_per_page = paginate(questions, request)
    return render(request, 'hot_questions.html', {
        'questions': questions_per_page,
    })


def new_question(request):
    return render(request, 'new_question.html', {})


def login(request):
    return render(request, 'login.html', {})


def signup(request):
    return render(request, 'signup.html', {})


def settings(request):
    return render(request, 'settings.html', {})


def question(request, qid):
    question = Question.objects.select_related().get(id=qid)
    answers = question.answer_set.order_by('-rating').all()
    answers_per_page = paginate(answers, request)
    return render(request, 'question.html', {
        'question': question,
        'answers':answers_per_page,
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


def paginate(objects_list, request, per_page=2):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(1)
    return objects
