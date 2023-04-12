from django.contrib.auth.models import Group, User
from rest_framework import serializers
from django_vacancies import models


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vacancy
        fields = "__all__"


class VacancySpecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vacancy
        fields = ["title", "salary"]
