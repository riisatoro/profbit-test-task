from django.core.management.base import (
    BaseCommand,
    CommandParser,
)
from django.db import connection
from products.models import Category, Product


class Command(BaseCommand):
    help = '''
        Update all products data.
        Use optional --category to update products in entered category.
        Use optional --product to update only one product.
    '''

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--category', type=str, help='Update products that belongs to category with entered name.')
        parser.add_argument('--product', type=str, help='Update concrete product by it\'s name.')
        return super().add_arguments(parser)
    
    def handle(self, *args, **options):
        category_name = options['category']
        product_name = options['product']

        

        prev_query_amount = len(connection.queries)

        self.stdout.write(f'Category {category_name}; Product {product_name}')
        self.stdout.write(f'It took {len(connection.queries) - prev_query_amount} database requests.')
