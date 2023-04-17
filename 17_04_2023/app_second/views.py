import re
import time

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from app_second import models
from django.contrib import messages


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.2f} seconds to execute")
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
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        print(password1, password2)

        if password1 != password2:
            # raise Exception("incorrect password")
            return render(request, "app_second/profile_register.html", context={"error": "incorrect password1"})
        # re_obj = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
        # compiling regex
        match_re = re.compile(reg)

        # searching regex
        # res_re = re.search(match_re, password1)
        # res_re = re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password1)
        # if not res_re:
            # raise Exception("incorrect password")
            # return render(request, "app_second/profile_register.html", context={"error": "incorrect password2"})

        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        return redirect("login")


def logout_f(request):
    logout(request)
    return redirect('login')


@time_it
def category_list_f(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        categories = cache.get("all_cats")
        if not categories:
            categories = models.Category.objects.all()
            cache.set("all_cats", categories)
        return render(request, "app_second/home.html", context={"categories": categories})


@time_it
def category_f(request: HttpRequest, slug) -> HttpResponse:
    if request.method == "GET":
        category_obj = models.Category.objects.get(slug=slug)
        name = f"Категория: {category_obj.name}"
        tovars = cache.get("tovar_" + str(slug))
        if not tovars:
            tovars = models.Tovar.objects.filter(category=category_obj)
            cache.set("tovar_" + str(slug), tovars, timeout=5)
        return render(request, "app_second/category.html", context={"tovars": tovars, "name": name})


@time_it
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
            return redirect()
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

