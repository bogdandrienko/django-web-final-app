from django.apps import AppConfig


class DjangoVacanciesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_vacancies'
    verbose_name = "Приложение для публикации и просмотра вакансий"
