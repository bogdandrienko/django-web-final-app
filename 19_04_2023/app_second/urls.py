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
    path('login/', views.login_f, name='login'),
    path('login/', views.login_f, name='category_list'),
    path('register/', views.register_f, name='register'),
    path('logout/', views.logout_f, name='logout'),
    path('category/<slug:slug>/', views.category_f, name='category'),
    path('tovar_detail/<int:pk>/', views.tovar_detail_f, name='tovar_detail'),
    path('', views.category_list_f, name='category_list'),
    path('home/', views.simple_VIEW, name='simple_VIEW'),
    # path('home/', views.BookListView.as_view(), name='simple_VIEW'),
    path('tovar_detail/<int:pk>/comment/', views.create_comment, name='create_comment'),
]
