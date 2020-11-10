from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

users = [
    {
        'name': f'Mr. TeaPot{idx}',

    } for idx in range(4)
]

tags = [
    {
        'tag': f'tag{idx}',

    } for idx in range(3)
]

questions = [
    {
        'id': idx,
        'title': f'title {idx}',
        'text': 'far from any road',
        'tags': tags,
        'rating': -2 + idx,
        'num_answers': 3,
        'author': 'Dr. Teapot',
        'data': 'Nov 11',
    } for idx in range(10)
]


answers = [
    {
        'id': idx,
        'text': 'far from any road',
        'rating': idx,
        'author': 'Mr. Black',
        'data': 'Dec 12',
    } for idx in range(3)
]

def hot_questions(request):
    questions_per_page = paginate(questions, request)
    return render(request, 'hot_questions.html', {
        'questions': questions_per_page,
        'tags': tags,
        'authors': users,
    })

def new_question(request):
    return render(request, 'new_question.html', {
        'tags': tags,
        'authors': users,})

def login(request):
    return render(request, 'login.html', {
        'tags': tags,
        'authors': users,})

def signup(request):
    return render(request, 'signup.html', {
        'tags': tags,
        'authors': users,})

def settings(request):
    return render(request, 'settings.html', {
        'tags': tags,
        'authors': users,})

def question(request, qid):
    question = questions[qid]
    answers_per_page = paginate(answers, request)
    return render(request, 'question.html', {
        'question': question,
        'answers':answers_per_page,
        'tags': tags,
        'authors': users,
    })

def tag_questions(request, sometag):
    questions_per_page = paginate(questions, request)
    return render(request, 'tag_questions.html', {
        'tag': sometag,
        'questions' : questions_per_page,
        'tags': tags,
        'authors': users,
    })

def index(request):
    questions_per_page = paginate(questions, request)
    return render(request, 'index.html', {
        'questions': questions_per_page,
        'tags': tags,
        'authors': users,
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