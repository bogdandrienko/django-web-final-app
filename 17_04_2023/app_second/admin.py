from django.contrib import admin
from app_second import models


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    """
    Настройки отображения, фильтрации и поиска модели:'Category' на панели администратора
    """

    list_display = (
        "name",
        "slug",
    )
    list_display_links = (
        "slug",
    )
    list_editable = (
        "name",
    )
    list_filter = (
        "name",
        "slug",
    )
    # filter_horizontal = (
    #     'users',
    # )
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "name",
                )
            },
        ),
        (
            "Техническое",
            {
                "fields": (
                    "slug",
                )
            },
        ),
    )
    search_fields = [
        "name",
        "slug",
    ]


admin.site.register(models.Category, CategoryAdmin)

class TovarAdmin(admin.ModelAdmin):
    """
    Настройки отображения, фильтрации и поиска модели:'Tovar' на панели администратора
    """

    list_display = (
        "title",
        # "slug",
        "category",
        "seller",
        "description",
        "price",
        'flag_good',
        "image",
        "created",
        'updated',
    )
    list_display_links = (
        "title",
        # "slug",
    )
    list_editable = (
        'flag_good',
    )
    list_filter = (
         "title",
        # "slug",
        "category",
        "seller",
        "description",
        "price",
        'flag_good',
        "image",
        "created",
        'updated',
    )
    # filter_horizontal = (
    #     'users',
    # )
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                     "title",
                        # "slug",
                        "category",
                        "seller",
                        "description",
                        "price",
                        "image",
                )
            },
        ),
        (
            "Техническое",
            {
                "fields": (
                    "created",
                    'flag_good',
                    'updated',
                )
            },
        ),
    )
    search_fields = [
        "title",
        # "slug",
    ]


admin.site.register(models.Tovar, TovarAdmin)


class ItemCommentAdmin(admin.ModelAdmin):
    """
    Настройки отображения, фильтрации и поиска модели:'ItemComment' на панели администратора
    """

    list_display = (
        "which_item",
        "who_commented",
        "text",
        "date",
    )
    list_display_links = (
        "which_item",
    )
    list_editable = (

    )
    list_filter = (
        "which_item",
        "who_commented",
        "date",
    )
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                     "which_item",
                     "who_commented",
                     "text",
                )
            },
        ),
        (
            "Техническое",
            {
                "fields": (
                    "date",
                )
            },
        ),
    )
    search_fields = [
        "which_item",
        "who_commented",
        "text",
        "date",
    ]

admin.site.register(models.ItemComment, ItemCommentAdmin)
