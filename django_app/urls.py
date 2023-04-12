from django.urls import re_path, path
from django.views.decorators.cache import cache_page
from django_app import views

urlpatterns = [
    # re_path(r"^$", cache_page(1 * 1)(views.HomeView.as_view()), name="home"),

    path("chat/", views.rooms, name="rooms"),
    path("chat/<slug:slug>/", views.room, name="room"),
]
