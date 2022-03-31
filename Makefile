build:
	docker-compose build

up:
	docker-compose up

products-create:
	docker exec -ti profbit-web python manage.py createproducts ${c} ${p}

products-update:
	docker exec -ti profbit-web python manage.py updateproducts --category=${c} --product=${p}

products-delete:
	docker exec -ti profbit-web python manage.py deleteproducts
