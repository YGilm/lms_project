LMS Project (Learning Management System)

Описание проекта

Проект "LMS" — бэкенд для системы управления обучением, разработанный с использованием Django REST Framework. Предназначен для создания, управления и распространения образовательного контента: курсов, уроков, тестов. Предоставляет API для взаимодействия с фронтенд-частью SPA веб-приложений. Разработан с акцентом на производительность, безопасность и масштабируемость.

Технологический стек

Python 3
Django и Django REST Framework
PostgreSQL
Redis
Docker и Docker Compose
Требования

Для запуска проекта необходимо установить:

Docker
Docker Compose
Инструкция по запуску:

Клонирование репозитория

git clone https://github.com/YGilm/lms_project.git
cd lms_project

Настройка переменных окружения
Создайте файл .env в корне проекта и добавьте в него необходимые переменные окружения в соответствии с примером example.env.

Запуск контейнеров

docker-compose up --build

Применение миграций
После запуска контейнеров выполните в новом терминале:

docker-compose exec app python manage.py migrate

Создание суперпользователя
docker-compose exec app python manage.py createsuperuser

Использование:

После запуска проект доступен по адресу http://localhost:8001/. API документация доступна по адресу http://localhost:8001/swagger/.
