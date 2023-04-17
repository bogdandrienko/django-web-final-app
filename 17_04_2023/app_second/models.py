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

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])


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
