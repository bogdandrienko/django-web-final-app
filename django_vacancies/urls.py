from django.urls import re_path
from django_vacancies import views

urlpatterns = [
    re_path(r"^api/vacansies/list/$", views.list),
    re_path(r"^api/vacansies/detail/(?P<pk>\d+)/$", views.detail),
    re_path(r"^api/vacansies/create/$", views.create),
    re_path(r"^api/vacansies/delete/(?P<pk>\d+)/$", views.delete),
    re_path(r"^api/vacansies/update/(?P<pk>\d+)/$", views.update),
]
