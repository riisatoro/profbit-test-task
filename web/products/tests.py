from random import randint
from django.test import TestCase
from unittest import mock

from products.models import Category, Product


NAMES_LIST = ['a', 'b', 'c', 'd', 'e', 'f']


class TestCategoryCreation(TestCase):

    def test_create_categories(self):
        category_amount = randint(10, 100)
        Category.randomly_create(category_amount)
        self.assertEqual(category_amount, Category.objects.count())

    @mock.patch('products.models.create_names', lambda _: NAMES_LIST)
    def test_create_duplicated_categories(self):
        Category.objects.all().delete()
        object_amount = len(NAMES_LIST)

        for _ in range(randint(10, 100)):
            Category.randomly_create(object_amount)

        self.assertEqual(object_amount, Category.objects.count())


class TestProductCreation(TestCase):
    def test_create_products(self):
        category_amount = randint(10, 100)
        product_amount = randint(10, 100)
        categories = Category.randomly_create(category_amount)

        products = Product.randomly_create(categories, product_amount)
        self.assertEqual(category_amount * product_amount, len(products))
    
    @mock.patch('products.models.create_names', lambda _: NAMES_LIST)
    def test_create_duplicates_products(self):
        object_amount = len(NAMES_LIST)
        categories = Category.randomly_create(object_amount)

        for _ in range(randint(10, 100)):
            Product.randomly_create(categories, object_amount)

        self.assertEqual(object_amount, Product.objects.count())
