from itertools import cycle
from random import choice, randint
from typing import List

from django.db.models import (
    CASCADE,
    CharField,
    DecimalField,
    ForeignKey,
    Model,
    PositiveIntegerField,
)
from django.core.validators import MinLengthValidator

from products.randomizers import create_names


class Category(Model):
    name = CharField(max_length=500, validators=[MinLengthValidator(3)], unique=True)

    def randomly_create(amount: int):
        names = create_names(amount)
        existed_categories = (
            Category.objects
            .filter(name__in=names)
            .values_list('name', flat=True)
        )
        uniq_categories = set(names) - set(existed_categories)

        return Category.objects.bulk_create([
            Category(name=name)
            for name in uniq_categories
        ])

    def __str__(self):
        return self.name


class Product(Model):
    PRODUCT_STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('in_stock', 'Out Of Stock'),
    ]

    name = CharField(max_length=500, validators=[MinLengthValidator(3)], unique=True)
    category = ForeignKey(to='Category', verbose_name='category', on_delete=CASCADE)
    price = DecimalField(max_digits=20, decimal_places=2)
    status = CharField(choices=PRODUCT_STATUS_CHOICES, max_length=128)
    remains = PositiveIntegerField()

    def randomly_create(categories: List[Category], amount: int):
        product_names = create_names(amount * len(categories))
        existed_products = (
            Product.objects.
            filter(name__in=product_names)
            .values_list('name', flat=True)
        )
        uniq_products = set(product_names) - set(existed_products)

        products_to_create = [
            Product(
                category=category,
                name=name,
                price=10,
                status=choice(Product.PRODUCT_STATUS_CHOICES)[0],
                remains=randint(1, 1000)
            )
            for category, name in zip(cycle(categories), uniq_products)
        ]
        return Product.objects.bulk_create(products_to_create)

    def __str__(self):
        return f'''{self.name} in {self.category} by {self.price}
            ({self.remains} amount, {self.status})'''
