from hashlib import md5
from itertools import cycle
from random import choice, randint, shuffle
from typing import List

from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db.models import (
    CASCADE,
    CharField,
    DecimalField,
    ForeignKey,
    PositiveIntegerField,
)

from products.mixins import ModelMixin
from products.randomizers import create_names, update_products
from cachers.cachers import update_cache


class Category(ModelMixin):
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

    class Meta:
        ordering = ('-created_at',)


class Product(ModelMixin):
    PRODUCT_STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('in_stock', 'Out Of Stock'),
    ]

    name = CharField(max_length=500, validators=[MinLengthValidator(3)], unique=True)
    category = ForeignKey(to='Category', verbose_name='category', on_delete=CASCADE)
    price = DecimalField(max_digits=20, decimal_places=2)
    status = CharField(choices=PRODUCT_STATUS_CHOICES, max_length=128)
    remains = PositiveIntegerField()

    @property
    def image(self):
        hash = md5(self.name.encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{hash}?d=retro'

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
                price=randint(1, 10000) / 100,
                status=choice(Product.PRODUCT_STATUS_CHOICES)[0],
                remains=randint(1, 1000)
            )
            for category, name in zip(cycle(categories), uniq_products)
        ]
        shuffle(products_to_create)
        return Product.objects.bulk_create(products_to_create)

    def randomly_update(category: str = None, product: str = None):
        filters = {}
        if category:
            filters = {'category__name': category}
        if product:
            filters = {'name': product}

        products = Product.objects.filter(**filters)
        updated_products = update_products(products)
        updated_products = Product.objects.bulk_update(updated_products, ['price', 'category', 'remains'])
        update_cache(products, Product.objects.all())

    def __str__(self):
        return f'''{self.name} in {self.category} by {self.price}
            ({self.remains} amount, {self.status})'''

    class Meta:
        ordering = ('-created_at',)
