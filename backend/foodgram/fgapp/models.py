from django.db import models
from users.models import User


class Tag(models.Model):
    tagname = models.TextField('Название')
    slug = models.SlugField('Слаг')

    class Meta:
        # ordering = ['-pub_date']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.tagname


class Ingredient(models.Model):
    product = models.CharField('Ингредиент', max_length=200)
    unit = models.CharField('Единица измерения', max_length=20)
    quantity = models.FloatField('Количество')

    class Meta:
        # ordering = ['-pub_date']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.product


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.TextField('Название', max_length=200)
    image = models.ImageField(
        'Фото',
        upload_to='fgapp/',
        blank=True
    )
    text = models.TextField('Описание')
    content = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.PROTECT
    )
    duration = models.IntegerField('Время приготовления')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title
