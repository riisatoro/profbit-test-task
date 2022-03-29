from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page

from products.views import ProductListView


urlpatterns = [
    path('', cache_page(settings.CACHE_TIME_SEC)(ProductListView.as_view()), name='products')
]
