from django.middleware.cache import FetchFromCacheMiddleware
from django.utils.cache import learn_cache_key

from products.models import CachedPages


class CustomFetchFromCacheMiddleware(FetchFromCacheMiddleware):
    
    def process_response(self, request, response):
        if request.method == 'GET':
            cache_key = learn_cache_key(request, response)
            page_number = request.GET.get('page', 0)
            CachedPages.objects.update_or_create(
                page_number=page_number,
                defaults={'cache_key': cache_key},
            )
        return response
