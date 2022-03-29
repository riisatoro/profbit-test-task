from django.core.management.base import (
    BaseCommand,
    CommandParser,
)
from django.db import connection
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Creates a categories and products for it with random values'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('categories', type=int)
        parser.add_argument('products', type=int)
        return super().add_arguments(parser)
    
    def handle(self, *args, **options):
        categories = options['categories']
        products = options['products']

        prev_query_amount = len(connection.queries)

        categories = Category.create_random_category(categories)
        products = Product.create_random_products(categories, products)

        self.stdout.write(f'Successfully added {len(categories)} categories and {products} products.')
        self.stdout.write(f'It took {len(connection.queries) - prev_query_amount} database requests.')
