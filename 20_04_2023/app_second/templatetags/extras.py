from django import template
from django.http import HttpRequest

from app_second import models as django_models

register = template.Library()


@register.filter(name="count_items_by_category_filter")
def count_items_by_category_filter(category_slug: str) -> int:
    category = django_models.Category.objects.get(slug=category_slug)
    return django_models.Tovar.objects.filter(category=category).count()


@register.simple_tag(takes_context=True)
def count_items_by_category_tag(context, category_slug: str) -> int:
    request: HttpRequest = context["request"]
    return django_models.Tovar.objects.filter(category__slug=category_slug).count()


@register.simple_tag(takes_context=True)
def get_username(context) -> str:
    request: HttpRequest = context["request"]
    user = request.user
    if user.is_authenticated:
        username = request.user.username
    else:
        username = "Аноним"
    return username
