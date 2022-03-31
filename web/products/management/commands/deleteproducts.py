from django.core.management.base import (
    BaseCommand,
)
from products.models import Category


class Command(BaseCommand):
    help = 'Delete all categories and products'
    
    def handle(self, *args, **options):
        Category.objects.all().delete()
        self.stdout.write('Products and Categories was cleared successfully.')
