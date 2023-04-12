from django.contrib import admin
from django_vacancies import models


# Register your models here.

class VacancyAdmin(admin.ModelAdmin):
    """
    Настройки отображения, фильтрации и поиска модели:'Vacancy' на панели администратора
    """

    list_display = (
        "company",
        "title",
        "salary",
        "experience",
        "work_type",
        "description",
        "created",
    )
    list_display_links = (
        "title",
        "description",
    )
    list_editable = (
        "created",
    )
    list_filter = (
        "company",
        "title",
        "salary",
        "experience",
        "work_type",
        "description",
        "created",
    )
    # filter_horizontal = (
    #     'users',
    # )
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "company",
                    "title",
                    "salary",
                    "experience",
                    "work_type",
                    "description",
                )
            },
        ),
        (
            "Техническое",
            {
                "fields": (
                    "created",
                )
            },
        ),
    )
    search_fields = [
        "title",
        "description",
    ]


admin.site.register(models.Vacancy, VacancyAdmin)
admin.site.register(models.Company)
