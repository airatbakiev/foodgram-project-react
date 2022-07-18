from turtle import title
from django.db import models


class Recipe(models.Model):
    title = models.TextField('Название', max_length=200)
    text = models.TextField('Описание', )
    duration = models.IntegerField('Время приготовления')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    image = models.ImageField(
        'Фото',
        upload_to='fgapp/',
        blank=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class Tag(models.Model):
    tagname = models.TextField('Название')
    slug = models.SlugField('Слаг')


class Ingredient(models.Model):
    product = models.CharField('Ингредиент', max_length=200)
    unit = models.CharField('Единица измерения', max_length=20)
    quantity = models.FloatField('Количество')
