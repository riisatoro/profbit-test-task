from random import randint
from unicodedata import category
from django.test import TestCase
from unittest import mock

from products.models import Category, Product


NAMES_LIST = ['a', 'b', 'c', 'd', 'e', 'f']


class TestCategoryCreation(TestCase):

    def test_create_categories(self):
        categories = Category.create_random_categories(10)
        db_categories = Category.objects.all()
        self.assertEqual(len(categories), len(db_categories))

    @mock.patch('products.models.create_names', lambda x: NAMES_LIST)
    def test_create_duplicated_categories(self):
        Category.objects.all().delete()
        for _ in range(randint(10, 100)):
            Category.create_random_categories(len(NAMES_LIST))

        self.assertEqual(Category.objects.count(), len(NAMES_LIST))
