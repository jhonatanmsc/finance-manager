install:
	pip install -r requirements.txt && pip install -r requirements-dev.txt && pre-commit install

tests:
	pytest -v

run:
	python manage.py runserver 0.0.0.0:8000

build_containers:
	docker compose --env-file .env build

start_containers:
	docker compose --env-file .env up --build

up_containers:
	docker compose --env-file .env up
