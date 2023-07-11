# Generated by Django 3.2 on 2023-07-11 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_title_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Укажите уникальный фрагмент URL-адреса', unique=True, verbose_name='URL-адрес'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(help_text='Укажите уникальный фрагмент URL-адреса', unique=True, verbose_name='URL-адрес'),
        ),
    ]
