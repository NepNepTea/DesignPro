# Generated by Django 4.2.16 on 2024-11-22 03:55

from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите категорию', max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(help_text='Введите описание заявки', max_length=1000)),
                ('plan', models.ImageField(upload_to='images/')),
                ('category', models.ManyToManyField(help_text='Выберите категорию заявки', to='studio.category')),
            ],
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='genre_name_case_insensitive_unique', violation_error_message='Жанр уже существует (совпадение без учета регистра)'),
        ),
    ]
