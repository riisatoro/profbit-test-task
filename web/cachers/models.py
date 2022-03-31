from django.db.models import CharField, PositiveIntegerField

from products.mixins import ModelMixin


class CachedPages(ModelMixin):
    page_number = PositiveIntegerField()
    cache_key = CharField(max_length=255)

    class Meta:
        unique_together = ('page_number', 'cache_key')
