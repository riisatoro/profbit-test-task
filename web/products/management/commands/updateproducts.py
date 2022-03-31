from django.core.management.base import (
    BaseCommand,
    CommandParser,
)
from django.db import connection
from products.models import Product


class Command(BaseCommand):
    help = '''
        Update all products data.
        Use optional --category to update products in entered category.
        Use optional --product to update only one product.
        Priority is given to the product name filter.
        To prevent console input errors, use singe comas to wrap category name.
        E. g ./manage.py updateproduct --category \'category_name\'\n --product \'product_name\'
    '''

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--category', type=str, help='Update products that belongs to category with entered name.')
        parser.add_argument('--product', type=str, help='Update concrete product by it\'s name.')
        return super().add_arguments(parser)
    
    def handle(self, *args, **options):
        category_name = options['category']
        product_name = options['product']

        prev_query_amount = len(connection.queries)

        Product.randomly_update(category_name, product_name)

        info_msg = '{} \'{}\' was updated successfully.'
        message = info_msg.format('All', 'products')
        if category_name:
            message = info_msg.format('Category', category_name)
        if product_name:
            message = info_msg.format('Product', product_name)

        self.stdout.write(message)
        self.stdout.write(f'It took {len(connection.queries) - prev_query_amount} database requests.')
