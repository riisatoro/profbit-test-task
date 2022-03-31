from django.conf import settings


def product_page_generator(products):
    total = products.count()
    pages = total // settings.PAGINATE_OBJECTS_BY
    pages = pages + 1 if total % settings.PAGINATE_OBJECTS_BY else pages

    for page in range(pages):
        yield (
            page + 1, 
            products[
                page*settings.PAGINATE_OBJECTS_BY
                :(page+1)*settings.PAGINATE_OBJECTS_BY
            ]
        )
