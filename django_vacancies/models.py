from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(300),
        ],
        unique=True,
        editable=True,
        blank=True,
        null=True,
        default="",
        verbose_name="Название компании",
        help_text='<small class="text-muted">CharField [1, 300]</small><hr><br>',
        max_length=300,
    )

    class Meta:
        app_label = "django_vacancies"
        ordering = ("-name",)
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return f"{self.name} ({self.id})"


class Vacancy(models.Model):
    company = models.ForeignKey(
        db_index=True,
        error_messages=False,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=True,
        default=None,
        verbose_name="Компания",
        help_text='<small class="text-muted">ForeignKey</small><hr><br>',
        to=Company,
        on_delete=models.SET_NULL,
    )
    title = models.CharField(
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(200),
        ],
        editable=True,
        blank=True,
        null=True,
        default="",
        verbose_name="Название вакансии",
        help_text='<small class="text-muted">CharField [1, 200]</small><hr><br>',
        max_length=200,
    )
    salary = models.DecimalField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(999999999),
        ],
        editable=True,
        blank=True,
        null=True,
        default=1.0,
        verbose_name="Зарплата",
        help_text='<small class="text-muted">DecimalField [1, 999999999]</small><hr><br>',
        decimal_places=3,
        max_digits=10,
    )
    experience = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(30),
        ],
        editable=True,
        blank=True,
        null=True,
        default=0,
        verbose_name="Опыт",
        help_text='<small class="text-muted">IntegerField [0, 30]</small><hr><br>',
    )
    work_type = models.CharField(
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(50),
        ],
        editable=True,
        blank=True,
        null=True,
        default="",
        verbose_name="График работы",
        help_text='<small class="text-muted">CharField [1, 50]</small><hr><br>',
        max_length=50,
    )
    description = models.TextField(
        db_index=True,
        error_messages=False,
        primary_key=False,
        validators=[
            MinLengthValidator(0),
            MaxLengthValidator(3000),
        ],
        unique=False,
        editable=True,
        blank=True,
        null=True,
        default="",
        verbose_name="Описание",
        help_text='<small class="text-muted">TextField [0, 3000]</small><hr><br>',
        max_length=3000,
    )
    created = models.DateTimeField(
        db_index=True,
        editable=True,
        blank=True,
        null=True,
        default=timezone.now,
        verbose_name="Дата и время создания",
        help_text='<small class="text-muted">DateTimeField</small><hr><br>',
        auto_now=False,
        auto_now_add=False,
    )

    class Meta:
        app_label = "django_vacancies"
        ordering = ("-created", "title")
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return f"{self.title} ({self.id}) {self.created}"
