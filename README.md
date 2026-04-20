# Yatube API

API для социальной сети Yatube - платформы для публикации постов и комментариев.

## Описание

Проект предоставляет REST API для управления публикациями, комментариями, группами и подписками. Реализована JWT-аутентификация, пагинация, поиск и фильтрация.

## Установка

1. Клонируйте репозиторий:
```bash
cd C:/Dev
git clone <your-repo-url>
```
2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate #для Linux/Mac
source venv/Scripts/activate #для Windows
```
3. Установите зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```
4. Выполните миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Запустите сервер:
```bash
python manage.py runserver
```

## Примеры запросов

Получение JWT токена:
```bash
POST /api/v1/jwt/create/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

Создание поста:
```bash
POST /api/v1/posts/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
    "text": "Мой первый пост!",
    "group": 1
}
```

Получение списка подписок:
```bash
GET /api/v1/follow/?search=username
Authorization: Bearer <your_access_token>
```