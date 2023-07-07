# Generated by Django 3.2 on 2023-07-07 22:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'категория', 'verbose_name_plural': 'категории'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'default_related_name': '%(class)ss', 'ordering': ('author',), 'verbose_name': 'комментарий', 'verbose_name_plural': 'комментарии'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('name',), 'verbose_name': 'жанр', 'verbose_name_plural': 'жанры'},
        ),
        migrations.AlterModelOptions(
            name='genretitle',
            options={'verbose_name': 'жанр произведения', 'verbose_name_plural': 'жанры произведений'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'default_related_name': '%(class)ss', 'ordering': ('author',), 'verbose_name': 'отзыв', 'verbose_name_plural': 'отзывы'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('name',), 'verbose_name': 'произведение', 'verbose_name_plural': 'произведения'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('username',), 'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='confirmation_code',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Укажите название', max_length=256, unique=True, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Укажите уникальный фрагмент URL-адреса', unique=True, verbose_name='уникальный фрагмент URL-адреса'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='дата публикации'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.review', verbose_name='отзыв'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='текст'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='Укажите название', max_length=256, unique=True, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(help_text='Укажите уникальный фрагмент URL-адреса', unique=True, verbose_name='уникальный фрагмент URL-адреса'),
        ),
        migrations.AlterField(
            model_name='genretitle',
            name='genre',
            field=models.ForeignKey(help_text='Выберите жанр', on_delete=django.db.models.deletion.CASCADE, to='reviews.genre', verbose_name='жанр'),
        ),
        migrations.AlterField(
            model_name='genretitle',
            name='title',
            field=models.ForeignKey(help_text='Выберите произведение', on_delete=django.db.models.deletion.CASCADE, to='reviews.title', verbose_name='произведение'),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Укажите значение от {MIN_SCORE} до {MAX_SCORE}.'), django.core.validators.MaxValueValidator(10, 'Укажите значение от {MIN_SCORE} до {MAX_SCORE}.')], verbose_name='рейтинг'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(verbose_name='текст'),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title', verbose_name='произведение'),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(help_text='Выберите категорию', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='категория произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, help_text='Добавьте описание произведения', null=True, verbose_name='описание произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(help_text='Выберите жанр', through='reviews.GenreTitle', to='reviews.Genre', verbose_name='жанр произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(help_text='Укажите название произведения', max_length=256, verbose_name='название произведения'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveIntegerField(db_index=True, help_text='Укажите год создания произведения', validators=[reviews.validators.validate_year], verbose_name='год создания произведения'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, help_text='Расскажите о себе.', verbose_name='биография'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('user', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='user', max_length=13, verbose_name='роль'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'Это имя пользователя уже существует.'}, max_length=150, unique=True, validators=[reviews.validators.validate_username], verbose_name='логин'),
        ),
    ]
