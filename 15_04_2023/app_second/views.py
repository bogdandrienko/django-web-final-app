import re

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from app_second import models


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


def category_list_f(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        categories = models.Category.objects.all()
        return render(request, "app_second/home.html", context={"categories": categories})


def category_f(request: HttpRequest, slug) -> HttpResponse:
    if request.method == "GET":
        category_obj = models.Category.objects.get(slug=slug)  # (1, 'Электроника', 'electro')
        tovars = models.Tovar.objects.filter(category=category_obj)  # [(1, 'Машина', '300000.00'), ...]
        name = f"Категория: {category_obj.name}"
        return render(request, "app_second/category.html", context={"tovars": tovars, "name": name})


def tovar_detail_f(request, pk):
    if request.method == "GET":
        tovar = models.Tovar.objects.get(id=pk)
        print(tovar)
        return render(request, "app_second/tovar.html", context={"tovar": tovar})
