import re

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.cache import cache, caches
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from app_second import models
from app_second import utils

DATABASE_CACHE = caches["default"]
RAM_CACHE = caches["special"]


@utils.decorator_for_request_inline
def login_f(request: WSGIRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'app_second/profile_login.html', context={})
    elif request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is None:
                return render(request, 'app_second/profile_login.html', context={"error": "User не найден"})
            login(request, user)
            return redirect('home')
        return render(request, 'app_second/profile_login.html', context={"error": "username or password пустые"})


@utils.decorator_for_request_inline
def register_f(request: WSGIRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "app_second/profile_register.html", context={})
    elif request.method == "POST":
        email = request.POST.get("email", "")
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if password1 != password2:
            return render(request, "app_second/profile_register.html", context={"error": "Пароли не совпадают!"})
        if not re.search(r"^.*(?=.{12,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$", password1):
            return render(request, "app_second/profile_register.html", context={"error": "Пароль не соответствует сложности!"})
        if not re.search(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email):
            return render(request, "app_second/profile_register.html", context={"error": "Почта неверная!"})

        User.objects.create_user(username=email, password=password1)
        return redirect("login")


@utils.decorator_for_request_inline
def logout_f(request: WSGIRequest) -> HttpResponse:
    if request.method == "GET":
        logout(request)
        return redirect('login')


@utils.decorator_for_request_inline
def home_f(request: WSGIRequest) -> HttpResponse:
    if request.method == "GET":
        categories = utils.custom_cache(
            cache_name=f"{request.path}_{request.method}", type_cache=RAM_CACHE, timeout=30,
            query=lambda: models.Category.objects.all()
        )
        return render(request, "app_second/home.html", context={"categories": categories})


@utils.decorator_for_request_inline
def category_f(request: HttpRequest, slug) -> HttpResponse:
    if request.method == "GET":
        _category = utils.custom_cache(
            cache_name=f"category_{slug}", type_cache=DATABASE_CACHE, timeout=30,
            query=lambda: models.Category.objects.get(slug=slug)
        )
        _items = utils.custom_cache(
            cache_name=f"category_item_{slug}", type_cache=DATABASE_CACHE, timeout=5,
            query=lambda: models.Tovar.objects.filter(category=_category)
        )
        return render(request, "app_second/category.html", context={"items": _items, "title": f"Категория: {_category.name}"})


@utils.decorator_for_request_inline
def user_items_f(request: HttpRequest, username: str) -> HttpResponse:
    if request.method == "GET":
        _user = User.objects.get(username=username)
        _items = utils.custom_cache(
            cache_name=f"user_items_{_user.username}", type_cache=DATABASE_CACHE, timeout=5,
            query=lambda: models.Tovar.objects.filter(seller=_user)
        )
        return render(request, "app_second/items_by_user.html", context={"username": _user.username, "items": _items})


@utils.decorator_for_request_inline
def create_f(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        _categories = utils.custom_cache(
            cache_name=f"create_Category", type_cache=DATABASE_CACHE, timeout=5,
            query=lambda: models.Category.objects.all()
        )
        return render(request, "app_second/create.html", context={"categories": _categories})
    elif request.method == "POST":
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        category = request.POST.get("category", "")
        price = request.POST.get("price", 0.0)
        image = request.FILES.get("image", None)
        item = models.Tovar.objects.create(
            title=title,
            category=models.Category.objects.get(slug=category),
            seller=request.user,
            description=description,
            flag_good=True,
            price=price,
            image=image,
        )
        return redirect("tovar_detail", pk=item.id)


@utils.decorator_for_request_inline
def tovar_detail_f(request, pk):
    if request.method == "GET":
        tovar = models.Tovar.objects.get(id=pk)
        comments = cache.get(str(tovar.id) + "detail_f")
        if not comments:
            comments = models.ItemComment.objects.filter(which_item_id=pk)
            cache.set(str(tovar.id) + "detail_f", comments, timeout=5)
        return render(request, "app_second/tovar.html", context={"tovar": tovar, "comments": comments})
    if request.method == "POST":
        try:
            comment_text = request.POST["comment"]
            comment_id = request.POST["comment_id"]
            get_comment = models.ItemComment.objects.get(comment_id)
            get_comment.text = comment_text
            get_comment.save()
        except Exception as error:
            messages.error(request, "Ошибка обновления комментария")
            print(f"Exception: {error}")
        return redirect("tovar_detail", pk)


@utils.decorator_for_request_inline
def create_comment(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "POST":
        comment_text = str(request.POST["comment"]).strip()
        if comment_text != '':
            try:
                models.ItemComment.objects.create(
                    who_commented=request.user,
                    which_item_id=pk,
                    text=comment_text
                )
            except Exception as error:
                messages.error(request, "Ошибка создания комментария")
                print(f"Exception: {error}")
        else:
            messages.info(request, "Комментарий не может быть пустым")
        return redirect("tovar_detail", pk=pk)
