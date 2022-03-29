from time import sleep

from django.conf import settings
from django.views.generic import ListView

from products.models import Product


class ProductListView(ListView):
    model = Product
    paginate_by = 50
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CACHE_TIME'] = settings.CACHE_TIME_SEC
        return context

    def get(self, *args, **kwargs):
        sleep(2)
        return super().get(*args, **kwargs)
