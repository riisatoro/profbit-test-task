from time import sleep

from django.conf import settings
from django.views.generic import ListView

from products.models import Product


class ProductListView(ListView):
    model = Product
    paginate_by = settings.PAGINATE_OBJECTS_BY
    allow_empty = True

    def get_queryset(self):
        sleep(2)
        return super().get_queryset()
