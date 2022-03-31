from django.middleware.cache import FetchFromCacheMiddleware
from django.utils.cache import learn_cache_key

from products.models import CachedPages


class CustomFetchFromCacheMiddleware(FetchFromCacheMiddleware):
    
    def process_response(self, request, response):
        if request.method == 'GET':
            cache_key = ":1:" + learn_cache_key(request, response)
            cached_page = request.GET.get('page', 0)
            CachedPages.objects.bulk_create(
                [CachedPages(page_number=cached_page, cache_key=cache_key)],
                ignore_conflicts=True,
            )
        return response
