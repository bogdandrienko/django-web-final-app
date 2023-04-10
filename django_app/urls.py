from django.urls import re_path
from django.views.decorators.cache import cache_page
from django_app import views

urlpatterns = [
    re_path(r"^$", cache_page(1 * 1)(views.HomeView.as_view()), name="home"),
]
