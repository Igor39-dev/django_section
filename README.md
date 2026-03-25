# Django Video App

Приложение для работы с видео, с REST API на DRF.

## Установка

### 1. Склонировать репозиторий:

```sh 
git clone (https://github.com/Igor39-dev/django_section.git)
```

cd project

### 2. Создать .env файл с переменными:
```sh
POSTGRES_DB=videos_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
DJANGO_SECRET_KEY=secret
DEBUG=True
```

### 3. Собрать Docker и запустить:
```sh
docker compose build
docker compose up
```

### 4. Выполнить миграции:
```sh
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

### 5. Доступ к админке: http://localhost:8000/staff/


## API:
| Endpoint                          | Method    | Описание                               |
| --------------------------------- | --------- | -------------------------------------- |
| `/v1/videos/`                     | GET       | Список видео с пагинацией              |
| `/v1/videos/`                     | POST      | Создание видео (только авторизованные) |
| `/v1/videos/{id}/`                | GET       | Получение конкретного видео            |
| `/v1/videos/{id}/`                | PUT/PATCH | Редактирование видео (автор или staff) |
| `/v1/videos/{id}/`                | DELETE    | Удаление видео (автор или staff)       |
| `/v1/videos/{id}/likes/`          | POST      | Поставить лайк                         |
| `/v1/videos/{id}/likes/`          | DELETE    | Убрать лайк                            |
| `/v1/videos/ids/`                 | GET       | Список всех ID видео (staff)           |
| `/v1/videos/statistics-subquery/` | GET       | Статистика по лайкам (subquery, staff) |
| `/v1/videos/statistics-group-by/` | GET       | Статистика по лайкам (group by, staff) |

