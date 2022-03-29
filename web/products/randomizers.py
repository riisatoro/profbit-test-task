from random import randint
from typing import List

from products.models import Product


def create_names(amount: int) -> List[str]:
    names = []
    while(len(names) < amount):
        names.append(
            ''.join([chr(randint(60, 120)) for _ in range(10)])
        )
    return names


def update_products(products: List[Product]) -> None:
    ...
