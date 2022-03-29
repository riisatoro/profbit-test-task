from django.core.management.base import (
    BaseCommand,
    CommandParser,
)
from django.db import connection
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Delete all categories and products'
    
    def handle(self, *args, **options):
        Category.objects.all().delete()
        self.stdout.write(f'Products and Categories was cleared successfully.')
