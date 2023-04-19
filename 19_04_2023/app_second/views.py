import re
import time
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.cache import cache, caches
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from app_second import models
from django.contrib import messages
from django.conf import settings
import datetime
from app_second import utils

DATABASE_CACHE = caches["default"]
RAM_CACHE = caches["special"]


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)

        print(f"{func.__name__} took {(time.time() - start_time):.5f} seconds to execute")
        return result

    return wrapper


def login_f(request):
    if request.method == 'GET':
        return render(request, 'app_second/profile_login.html', context={})
    elif request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is None:
                return render(request, 'app_second/profile_login.html', context={"error": "User не найден"})
            login(request, user)
            return redirect('category_list')
        return render(request, 'app_second/profile_login.html', context={"error": "username or password пустые"})


def register_f(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "app_second/profile_register.html", context={})

    elif request.method == "POST":
        # todo чтение из формы
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        # todo чтение из формы

        # todo сравнение паролей
        if password1 != password2:
            return render(request, "app_second/profile_register.html", context={"error": "incorrect password1"})
        # todo сравнение паролей

        # todo регистрация пользователя
        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        # todo регистрация пользователя

        # todo перенаправление пользователя
        return redirect("login")
        # todo перенаправление пользователя


def logout_f(request):
    logout(request)
    return redirect('login')


from django.views.generic import TemplateView, ListView, FormView


# class BookListView(LoginRequiredMixin, ListView, FormView):
#     model = models.Category
#     template_name = "app_second/home.html"
#
#
# class HomeView(TemplateView):
#     template_name = "app_second/404.html"

@utils.decorator_for_request_inline
def simple_VIEW(request):
    categories = utils.custom_cache(type_cache=RAM_CACHE, cache_name=f"{request.path}_{request.method}", timeout=30,
                                    query=lambda: models.Category.objects.all())
    return render(request, "app_second/home.html", context={"categories": categories})


class God:
    @utils.decorator_for_request_inline
    def get(self):
        pass

    @utils.decorator_for_request_inline
    def post(self):
        pass


@utils.decorator_for_request_inline
def category_f(request: HttpRequest, slug) -> HttpResponse:
    if request.method == "GET":
        category_obj = models.Category.objects.get(slug=slug)
        name = f"Категория: {category_obj.name}"

        tovars = utils.custom_cache(
            type_cache=DATABASE_CACHE,
            cache_name="tovar_" + str(slug),
            timeout=5,
            query=lambda: models.Tovar.objects.filter(category=category_obj)
        )

        return render(request, "app_second/category.html", context={"tovars": tovars, "name": name})


@utils.decorator_for_request_inline
def category_list_f(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        categories = utils.custom_cache(
            type_cache=DATABASE_CACHE,
            cache_name="all_cats",
            timeout=60,
            query=lambda: models.Category.objects.all()
        )

        return render(request, "app_second/home.html", context={"categories": categories})


# @time_it
def tovar_detail_f(request, pk):
    if request.method == "GET":
        tovar = models.Tovar.objects.get(id=pk)

        comments = cache.get(str(tovar.id) + "detail_f")
        if not comments:
            comments = models.ItemComment.objects.filter(which_item_id=pk)
            cache.set(str(tovar.id) + "detail_f", comments, timeout=5)

        return render(request, "app_second/tovar.html",
                      context={"tovar": tovar, "comments": comments})
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
