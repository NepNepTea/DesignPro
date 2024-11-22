from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

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
    category = models.ManyToManyField(Category, help_text="Выберите категорию заявки")
    plan = models.ImageField(upload_to ='images/')
    status = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('plea-detail', args=[str(self.id)])

    def __str__(self):
        return self.name