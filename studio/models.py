from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from datetime import date

class Category(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Введите категорию"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message = "Жанр уже существует (совпадение без учета регистра)"
            ),
        ]

class Plea(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, help_text="Введите описание заявки")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, help_text="Выберите категорию заявки")
    plan = models.ImageField(upload_to ='images/', null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creationDate = models.DateField(default=date.today)
    comentary = models.TextField(max_length=1000, null=True)
    design = models.ImageField(upload_to ='images/', null=True)

    LOAN_STATUS = (
        ('n', 'Новая'),
        ('c', 'Выполнено'),
        ('i', 'принято в работу')
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='n', help_text='Статус заявки')

    def get_absolute_url(self):
        return reverse('plea-detail', args=[str(self.id)])

    def __str__(self):
        return self.name