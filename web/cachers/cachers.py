from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from cachers.generators import product_page_generator
from cachers.models import CachedPages
    

def _update_cache_page(page_number: int, product_list):
    cache_key = CachedPages.objects.filter(page_number=page_number).first()
    if not cache_key:
        return

    cache_key = cache_key.cache_key
    template = cache.get(cache_key)
    if not template:
        return

    pages = Paginator(product_list, settings.PAGINATE_OBJECTS_BY)
    context = pages.page(page_number)
    template.content = render_to_string('products/product_list.html', {'page_obj': context})
    cache.set(cache_key, template)

def update_cache(products, all_products):
    products = set(products)
    pages = product_page_generator(all_products)

    for page, obj_list in pages:
        if products.intersection(obj_list):
            _update_cache_page(page, all_products)
