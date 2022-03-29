from random import randint


def create_names(amount: int):
    names = []
    while(len(names) < amount):
        names.append(
            ''.join([chr(randint(60, 120)) for _ in range(10)])
        )
    return names
