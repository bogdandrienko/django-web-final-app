from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(verbose_name="Наименование категории товаров", max_length=200)
    slug = models.SlugField(verbose_name="Ссылка на категорию товаров", max_length=200, unique=True)

    # avatar
    # descrp
    class Meta:
        app_label = "app_second"
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def count_items_by_category(self) -> int:
        return Tovar.objects.filter(category=self).count()


class Tovar(models.Model):
    title = models.CharField(verbose_name="Наименование товара", max_length=200)
    # slug = models.SlugField(verbose_name="Ссылка на товар", max_length=200, unique=True)
    category = models.ForeignKey(Category, null=True, default=None, on_delete=models.SET_NULL)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    flag_good = models.BooleanField(default=False, verbose_name="Одобрено")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='ads/%Y/%m/%d/', blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "app_second"
        ordering = ('-created',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title

    def get_comments(self):
        return ItemComment.objects.filter(which_item=self)

    def get_absolute_url(self):
        return reverse('ad_detail', args=[self.slug])


class ItemComment(models.Model):
    which_item = models.ForeignKey(Tovar, on_delete=models.CASCADE)
    who_commented = models.ForeignKey(User, on_delete=User)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(f"{self.who_commented}|{self.which_item}")

    class Meta:
        app_label = "app_second"
        ordering = ('-date',)
        verbose_name = 'Комментарий к товару'
        verbose_name_plural = 'Комментарии к товару'


class LoggingModel(models.Model):
    """
    Модель, которая содержит логирование действий и ошибок django
    """

    LEVELS = [
        ("action", "Действие"),
        ("low", "Низкий"),
        ("middle", "Средний"),
        ("high", "Высокий"),
        ("critical", "Критический"),
    ]
    level = models.CharField(
        max_length=10,
        choices=LEVELS,
        default="critical",
    )
    user = models.ForeignKey(
        db_index=True,
        error_messages=False,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=True,
        default=None,
        verbose_name="Пользователь",
        help_text='<small class="text-muted">ForeignKey</small><hr><br>',
        to=User,
        on_delete=models.SET_NULL,
    )
    ip = models.GenericIPAddressField(
        db_index=True,
        error_messages=False,
        primary_key=False,
        validators=[
            MinLengthValidator(0),
            MaxLengthValidator(300),
        ],
        unique=False,
        editable=True,
        blank=True,
        null=True,
        default=None,
        verbose_name="Ip адрес",
        help_text='<small class="text-muted">ip[0, 300]</small><hr><br>',
        max_length=300,
        protocol="both",
        unpack_ipv4=False,
    )
    path = models.SlugField(
        db_index=True,
        error_messages=False,
        primary_key=False,
        validators=[
            MinLengthValidator(0),
            MaxLengthValidator(300),
        ],
        unique=False,
        editable=True,
        blank=True,
        null=True,
        default="",
        verbose_name="Путь",
        help_text='<small class="text-muted">SlugField [0, 300]</small><hr><br>',
        max_length=300,
        allow_unicode=False,
    )
    method = models.SlugField(
        db_index=True,
        error_messages=False,
        primary_key=False,
        validators=[
            MinLengthValidator(0),
            MaxLengthValidator(300),
        ],
        unique=False,
        editable=True,
        blank=True,
        null=True,
        default="",
        verbose_name="Метод",
        help_text='<small class="text-muted">SlugField [0, 300]</small><hr><br>',
        max_length=300,
        allow_unicode=False,
    )
    text = models.TextField(
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
        verbose_name="Текст ошибки/исключения/ответа",
        help_text='<small class="text-muted">TextField [0, 3000]</small><hr><br>',
        max_length=3000,
    )
    created = models.DateTimeField(
        db_index=True,
        error_messages=False,
        primary_key=False,
        unique=False,
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
        app_label = "auth"
        ordering = ("-created",)
        verbose_name = "Логирование"
        verbose_name_plural = "Логирование"

    def __str__(self):
        if self.user:
            username = self.user.username
        else:
            username = "Аноним"
        return f"{self.created} | {username} | {self.path}"
