# Simple shop with caching
Small single-page shop for investigating about django cache framework.


## Requirements

* Docker 20.10
* Docker-compose 1.25


## Setup & build
* Create a .env file using .env.example
  * Use default postgres credentials - `postgres` for username & password
* Run docker build:  
  * `make build` or `docker-compose build`
* In addition - install poetry dependencies:
    * `pip install poetry`
    * `poetry install`


## Runing the application
* Run with docker:
  * `make up` or `docker-compose up`
* Run locally:
    * `poetry run python manage.py migrate`
    * `poetry run python manage.py runserver`

Default application url: ` 127.0.0.1:8000 `


# Project description
This is a single page app, build on Django & Django Templates. For caching it uses DatabaseCaching.

The goal is to update cache if some product data was updated. For High-load emulation, in `get_queryset` method `time.sleep(2)` is used to make a long-time loaded page (about 2 secongs), that should be cached.  

The expected workflow of whole project should be:
* page is rendered on server > 2 sec and cached;
* product data is updated;
* page is refreshed, loaded from cache (< 2 sec) **but** product info on page is updated.

The most detailed explanation: ...soon...

To make app testing more simple, you could use the following commands:
* `make products-create c=CATEGORY_AMOUNT p=PRODUCT_AMOUNT` or `python manage.py createproducts CATEGORY_AMOUNT PRODUCT_AMOUNT`  
Create a product for each category in amount, that was entered.

* `make products-update [c=CATEGORY_NAME] [p=PRODUCT_NAME]` or `python manage.py updateproducts [--category=CATEGORY_NAME] [--product=PRODUCT_NAME]`  
Apply random values to products. By default all products will be updated with random values. In addition, you could set optional `CATEGORY_NAME` or `PRODUCT_NAME` to update either products in single category, or single product. If both values is supplied, only single product will be updated.

* `make products-delete` or `python manage.py deleteproducts`  
Delete all products and categories.

Additionaly, each command shows amount of database request spent.
