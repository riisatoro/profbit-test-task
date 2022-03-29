from random import choice

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

    def create_random_categories(amount: int):
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

    def __str__(self):
        return f'''{self.name} in {self.category} by {self.price}
            ({self.remains} amount, {self.status})'''
