.PHONY: up down makemigrations migrate

up:
	docker-compose up --build

down:
	docker-compose down

makemigrations:
	alembic revision --autogenerate -m "$(m)"

migrate:
	alembic upgrade head