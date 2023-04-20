"""
URL configuration for settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, re_path
from app_second import views

urlpatterns = [
    # todo auth
    path('login/', views.login_f, name='login'),
    path('logout/', views.logout_f, name='logout'),
    path('register/', views.register_f, name='register'),
    #
    # todo base
    path('', views.home_f, name=''),
    path('home/', views.home_f, name='home'),
    path('category/<slug:slug>/', views.category_f, name='category'),
    path('items/<str:username>/', views.user_items_f, name='items'),
    path('create/', views.create_f, name='create'),

    path('tovar_detail/<int:pk>/', views.tovar_detail_f, name='tovar_detail'),
    path('tovar_detail/<int:pk>/comment/', views.create_comment, name='create_comment'),
]
