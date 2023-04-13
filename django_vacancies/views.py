from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from django_vacancies import models, serializers


# Create your views here.
@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def list(request: Request) -> Response:
    search = request.GET["search"]
    experience = request.GET["experience"]
    sort = request.GET["sort"]

    print(sort)

    vacancies_obj = models.Vacancy.objects.filter(title__icontains=search, experience__gte=int(experience))
    """ SELECT id, title, description WHERE title LIKE %back% """
    # back_end
    # endback
    # endback_end

    print(vacancies_obj)
    if sort == "salary_asc":
        vacancies_obj = vacancies_obj.order_by("salary")
    elif sort == "salary_desc":
        vacancies_obj = vacancies_obj.order_by("-salary")
    elif sort == "by_created":
        vacancies_obj = vacancies_obj.order_by("-created")
    else:
        pass
    print(vacancies_obj)


    vacancies_json = serializers.VacancySerializer(instance=vacancies_obj, many=True).data
    # data = [
    #     {"id": 1, "title": "Продавец", "salary": 5000},
    #     {"id": 2, "title": "Разносчик", "salary": 2000},
    #     {"id": 3, "title": "Повар", "salary": 3000},
    #     {"id": 4, "title": "Курьер", "salary": 8000},
    #     {"id": 5, "title": "Официант", "salary": 3000},
    # ]
    return Response(data=vacancies_json, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def detail(request: Request, pk: int) -> Response:
    vacancies_obj = models.Vacancy.objects.get(id=pk)
    vacancies_json = serializers.VacancySerializer(instance=vacancies_obj, many=False).data
    return Response(data=vacancies_json, status=status.HTTP_200_OK)


@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
def create(request: Request) -> Response:
    # {"title": "Яичница 1", "salary": 3000} - JSON

    title = request.data["title"]
    salary = request.data["salary"]
    models.Vacancy.objects.create(
        title=title,
        salary=salary,
    )
    return Response(data={"message": "успешно создано"}, status=status.HTTP_201_CREATED)


@api_view(http_method_names=["DELETE"])
@permission_classes([AllowAny])
def delete(request: Request, pk: int) -> Response:
    models.Vacancy.objects.get(id=pk).delete()
    return Response(data={"message": "успешно удалено"}, status=status.HTTP_200_OK)


@api_view(http_method_names=["PUT"])
@permission_classes([AllowAny])
def update(request: Request, pk: int) -> Response:
    # {"title": "Яичница", "salary": 777} - JSON

    vacancy = models.Vacancy.objects.get(id=pk)

    title = request.data["title"]
    salary = request.data["salary"]

    vacancy.title = title
    vacancy.salary = salary
    vacancy.save()

    return Response(data={"message": "успешно обновлено"}, status=status.HTTP_200_OK)
