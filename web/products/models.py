from itertools import cycle
from random import choice, randint, shuffle
from re import template
from typing import List

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator
from django.core.validators import MinLengthValidator
from django.db.models import (
    CASCADE,
    CharField,
    DecimalField,
    ForeignKey,
    Model,
    PositiveIntegerField,
    DateTimeField,
)
from django.template.loader import render_to_string

from products.randomizers import create_names, update_products


def product_paginator(products):
    total = products.count()
    pages = total // settings.PAGINATE_OBJECTS_BY
    pages = pages + 1 if total % settings.PAGINATE_OBJECTS_BY else pages

    for page in range(pages):
        yield (
            page, 
            products[
                page*settings.PAGINATE_OBJECTS_BY
                :(page+1)*settings.PAGINATE_OBJECTS_BY
            ]
        )

def update_products_page_cache(products, all_products):
    products = set(products)
    pages = product_paginator(all_products)

    for page, obj_list in pages:
        if products.intersection(obj_list):
            update_cache_page(page + 1, all_products)


def update_cache_page(page: int, object_list):
    cache_key = CachedPages.objects.filter(page_number=page).first()
    if not cache_key:
        return

    pages = Paginator(object_list, settings.PAGINATE_OBJECTS_BY)
    context = pages.page(page)
    template_response = cache.get(cache_key.cache_key)
    if not template_response:
        return

    template_response.content = render_to_string('products/product_list.html', {'page_obj': context})
    cache.set(cache_key.cache_key, template_response)



class ModelMixin(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
        update_products_page_cache(products, Product.objects.all())

    def __str__(self):
        return f'''{self.name} in {self.category} by {self.price}
            ({self.remains} amount, {self.status})'''

    class Meta:
        ordering = ('-created_at',)


class CachedPages(ModelMixin):
    page_number = PositiveIntegerField()
    cache_key = CharField(max_length=255)

    class Meta:
        unique_together = ('page_number', 'cache_key')
