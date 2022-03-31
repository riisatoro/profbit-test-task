from random import randint, choice
from typing import List


LETTERS = [chr(code) for code in list(range(65, 90)) + list(range(97, 122))]


def create_names(amount: int) -> List[str]:
    names = []
    while(len(names) < amount):
        names.append(
            ''.join([choice(LETTERS) for _ in range(10)])
        )
    return names


def update_products(products):
    for product in products:
        product.price = randint(1, 10000) / 10
        product.status = choice(product.PRODUCT_STATUS_CHOICES)[0]
        product.remains = randint(1, 10000)

    return products
