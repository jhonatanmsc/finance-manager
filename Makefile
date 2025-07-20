install:
	pip install -r requirements.txt && pip install -r requirements-dev.txt && pre-commit install

run:
	python manage.py runserver 0.0.0.0:8000

start_containers:
	docker compose --env-file .env up --build
