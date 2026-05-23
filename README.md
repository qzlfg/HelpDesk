# HelpDesk API

## Запуск (через Docker)

1. Склонируйте репозиторий
2. Создайте файл `.env` (опционально)
3. Выполните `docker-compose up --build`
4. Документация: http://localhost:8000/docs

## Команды

- `make up` – запуск всех сервисов
- `make down` – остановка
- `make makemigrations m="comment"` – создание миграции
- `make migrate` – применение миграций

## Тестирование