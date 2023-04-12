from django.urls import re_path, include, path
from django.views.generic import TemplateView
from rest_framework import permissions, routers
from django_api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Примеры маршрутов API",
        default_version="v1",
        # description="Test description",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"group", views.GroupViewSet)

urlpatterns = [
    re_path(r"token/$", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    re_path(r"token/refresh/$", TokenRefreshView.as_view(), name="token_refresh"),

    re_path(r"user/register/$", views.user_register_f, name="user_register_f"),

    re_path(r"swagger(?P<format>\.json|\.yaml)/$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    re_path(r"", include(router.urls)),


    re_path(r"post/create/$", views.post_create_f),                 # C
    re_path(r"post/(?P<pk>\d+)/$", views.post_read_f),              # R
    re_path(r"post/list/$", views.post_list_f),                     # R
    re_path(r"post/update/$", views.post_update_f),                 # U
    re_path(r"post/(?P<pk>\d+)/delete/$", views.post_delete_f),     # D
]
