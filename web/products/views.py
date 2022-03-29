from time import sleep

from django.views.generic import ListView

from products.models import Product


class ProductListView(ListView):
    model = Product
    paginate_by = 50
    allow_empty = True

    def get(self, *args, **kwargs):
        sleep(2)
        return super().get(args, kwargs)
