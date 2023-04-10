# Generated by Django 4.2 on 2023-04-10 14:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(blank=True, default='', help_text='<small class="text-muted">CharField [0, 12]</small><hr><br>', max_length=12, null=True, validators=[django.core.validators.MinLengthValidator(0), django.core.validators.MaxLengthValidator(12)], verbose_name='Мобильный')),
                ('avatar', models.ImageField(blank=True, default='default/account/default_avatar.jpg', help_text='<small class="text-muted"ImageField [jpg, png]</small><hr><br>', max_length=200, null=True, upload_to='uploads/admin/account/avatar', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png'])], verbose_name='Изображение')),
                ('user', models.OneToOneField(blank=True, default=None, help_text='<small class="text-muted">ForeignKey</small><hr><br>', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='django_app.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_added',),
            },
        ),
        migrations.CreateModel(
            name='LoggingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.SlugField(blank=True, default='', error_messages=False, help_text='<small class="text-muted">SlugField [0, 300]</small><hr><br>', max_length=300, null=True, validators=[django.core.validators.MinLengthValidator(0), django.core.validators.MaxLengthValidator(300)], verbose_name='Имя пользователя')),
                ('ip', models.GenericIPAddressField(blank=True, db_index=True, default=None, error_messages=False, help_text='<small class="text-muted">ip[0, 300]</small><hr><br>', null=True, validators=[django.core.validators.MinLengthValidator(0), django.core.validators.MaxLengthValidator(300)], verbose_name='Ip адрес')),
                ('path', models.SlugField(blank=True, default='', error_messages=False, help_text='<small class="text-muted">SlugField [0, 300]</small><hr><br>', max_length=300, null=True, validators=[django.core.validators.MinLengthValidator(0), django.core.validators.MaxLengthValidator(300)], verbose_name='Путь')),
                ('method', models.SlugField(blank=True, default='', error_messages=False, help_text='<small class="text-muted">SlugField [0, 300]</small><hr><br>', max_length=300, null=True, validators=[django.core.validators.MinLengthValidator(0), django.core.validators.MaxLengthValidator(300)], verbose_name='Метод')),
                ('text', models.TextField(blank=True, db_index=True, default='', error_messages=False, help_text='<small class="text-muted">TextField [0, 3000]</small><hr><br>', max_length=3000, null=True, validators=[django.core.validators.MinLengthValidator(0), django.core.validators.MaxLengthValidator(3000)], verbose_name='Текст ошибки/исключения/ответа')),
                ('created', models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now, error_messages=False, help_text='<small class="text-muted">DateTimeField</small><hr><br>', null=True, verbose_name='Дата и время создания')),
                ('user', models.ForeignKey(blank=True, default=None, error_messages=False, help_text='<small class="text-muted">ForeignKey</small><hr><br>', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Admin 5, Логи',
                'ordering': ('-created',),
            },
        ),
    ]