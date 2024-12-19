"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from .forms import ReviewForm
from .forms import BlogForm

from .models import Works
from django.db import models 
from .models import Blog

from .models import Comment 
from .forms import CommentForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request, 
        'app/links.html',
        {
            'title': 'Полезные ссылки:',
            'year': datetime.now().year,
        }
     )

def review(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    data = None
    rating = {'1': 'Ужасно',
              '2': 'Плохо',
              '3': 'Нормально',
              '4': 'Неплохо',
              '5': 'Хорошо'
    }

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['rating'] = rating[ form.cleaned_data['rating'] ]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = ReviewForm()

    return render(
        request,
        'app/review.html',
        {
            'form':form,
            'data':data
        }
    )

def registration(request):
    """Renders the registration page."""

    if request.method == "POST":  # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False  # запрещен вход в админ. раздел
            reg_f.is_active = True  # активный пользователь
            reg_f.is_superuser = False  # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now()  # дата последней авторизации

            regform.save()  # сохраняем изменения после добавления полей

            return redirect('home')  # переадресация на главную страницу после авторизации
        else:
            return render(
                request,
                'app/registration.html',
                {
                    'regform': regform,
                    'year': datetime.now().year,
                }
            )
    else:
        regform = UserCreationForm()  # создание объекта формы для ввода данных
        return render(
            request,
            'app/registration.html',
            {
                'regform': regform,
                'year': datetime.now().year,
            }
        )

def blog(request):
    """Renders the blog page"""
    posts = Blog.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',
            'posts': posts,
            'year': datetime.now().year,
        }
    )

def blogpost(request, parametr): 
    """Renders the blogpost page"""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = post_1
            comment_f.save()

            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()  # Инициализация формы для GET-запросов

    return render(
        request, 
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )

def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
       request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',

            'year': datetime.now().year,
        }
    )

def videopost(request):
    """Renders the videopost page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'year':datetime.now().year,
        }
    )

def works(request):
    works = Works.objects.all()
    return render(request, 'app/works.html', {'works': works})