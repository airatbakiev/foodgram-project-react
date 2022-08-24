import csv
from django.core.management.base import BaseCommand

from fgapp.models import Ingredient, Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        '''Импорт заготовленных данных из папки data'''
        pk = 1
        with open(
            './data/ingredients.csv', newline='', encoding='utf-8'
        ) as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            for row in datareader:
                ingredient = Ingredient(
                    id=pk,
                    name=row['name'],
                    measurement_unit=row['measurement_unit'],
                )
                ingredient.save()
                pk += 1
        pk = 1
        with open(
            './data/tags.csv', newline='', encoding='utf-8'
        ) as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            for row in datareader:
                tag = Tag(
                    id=pk,
                    name=row['name'],
                    color=row['color'],
                    slug=row['slug'],
                )
                tag.save()
                pk += 1
