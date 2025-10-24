<div id="header" align="center">
<img src="https://img.shields.io/badge/Python-black?style=for-the-badge&logo=python&logoColor=yellow"/>&nbsp;
<img src="https://img.shields.io/badge/FastAPI-black?style=for-the-badge&logo=fastapi&logoColor=009688"/>&nbsp;
<img src="https://img.shields.io/badge/SQLAlchemy-black?style=for-the-badge&logo=sqlalchemy&logoColor=D71F00"/>&nbsp;
<img src="https://img.shields.io/badge/PostgreSQL-black?style=for-the-badge&logo=PostgreSQL&logoColor=4169E1"/>&nbsp;
<img src="https://img.shields.io/badge/Redis-black?style=for-the-badge&logo=Redis&logoColor=FF4438"/>
<img src="https://img.shields.io/badge/Celery-black?style=for-the-badge&logo=Celery&logoColor=37814A"/>
<img src="https://img.shields.io/badge/PyTest-black?style=for-the-badge&logo=PyTest&logoColor=0A9EDC"/>
<img src="https://img.shields.io/badge/Docker-black?style=for-the-badge&logo=docker&logoColor=#07F"/>&nbsp;
<img src="https://img.shields.io/badge/Nginx-black?style=for-the-badge&logo=nginx&logoColor=#00b341"/>&nbsp;
</div>


# Сервис бронирования отелей

Современный REST API для системы бронирования отелей на фреймворке FastAPI с полным стеком технологий.

## 🎯 Особенности проекта

### 🔐 Аутентификация
- Регистрация/вход (OAuth2 с JWT-токенами)
- Хеширование паролей

### 🏨 Управление данными
- CRUD для отелей, номеров, бронирований
- Связи many-to-many номера-удобства
- Валидация данных и бизнес-правил

### 📅 Бронирование
- Проверка доступности номеров на даты
- Расчет стоимости бронирования
- Автоматические уведомления о заезде

  **Внимание! Чтобы бронировать номера нужно зарегистрироваться и выполнить вход в систему!**

### 🖼️ Медиа
- Загрузка изображений отелей
- Автоматическое создание ресайзов изображений
- Фоновая обработка через Celery

### 🔍 Поиск и фильтрация

Система поддерживает сложные запросы на поиск отелей и номеров:

- Поиск отелей по названию и местоположению
- Фильтрация по датам заезда/выезда
- Автоматический расчет доступных номеров
- Пагинация результатов

### 🛡️ Безопасность
- Валидация всех входящих данных
- Хеширование паролей с bcrypt
- JWT-токены с настройкой времени жизни
- Защита от SQL-инъекций через SQLAlchemy
- Валидация MIME-типов и размеров файлов
- Ограничение количества запросов в секунду на уровне Nginx

## 🚀 Технологии

- **FastAPI** - современный высокопроизводительный веб-фреймворк
- **PostgreSQL** - основная база данных
- **SQLAlchemy 2.0** - асинхронный ORM
- **Alembic** - миграции базы данных
- **JWT** - аутентификация и авторизация
- **Redis** - кэширование и брокер сообщений для Celery
- **Celery** - фоновые задачи
- **Pytest** - тестирование
- **Ruff** - линтинг и форматирование
- **PyRight** - статический типизатор
- **Docker** - контейнеризация
- **Nginx** - прокси и SSL терминация

## 🏗️ Архитектура

### 📁 Архитектура проекта

    ├─ src/
    │   ├── api/                 # Роутеры FastAPI (Presentation Layer)
    │   ├── connectors/          # Infrastructure Layer (Redis connector)
    │   ├── models/              # Domain Layer
    │   ├── repositories/        # Data Access Layer (Repository Pattern)
    │   │        └── mappers/    # Data Mapper Pattern
    │   ├── schemas/             # DTO Layer
    │   ├── services/            # Business Layer (Service Layer Pattern)
    │   ├── static/
    │   │      └── images/
    │   ├── tasks/               # Background Tasks (Command Pattern)
    │   └── utils/               # (Unit of Work Pattern, Strategy Pattern)
    └── tests


### 🗄️ Структура базы данных
    hotels (id, title, location)
    rooms (id, hotel_id, title, description, price, quantity)
    users (id, email, hashed_password)
    bookings (id, user_id, room_id, date_from, date_to, price)
    facilities (id, title)
    rooms_facilities (id, room_id, facility_id)

### Принципы проектирования
1. 🧹 **Чистая Архитектура** - используется многослойная архитектура (Layered Architecture), разделяющая код на независимые слои Domain, Application, Infrastructure, Presentation:
- **Domain Layer** (`models/`) - Сущности предметной области и бизнес-правила
- **Application Layer** (`services/`, `schemas/`) - Use Cases и бизнес-логика
- **Infrastructure Layer** (`repositories/`, `connectors/`) - Внешние системы и БД
- **Presentation Layer** (`api/`) - API endpoints<br><br>

  `Presentation Layer (API) → Business Layer (Services) → Data Access Layer (Repositories) → Database`<br><br>

  Каждый слой зависит только от внутренних слоев, что обеспечивает:
  - Независимость бизнес-логики от фреймворков
  - Легкое тестирование компонентов
  - Гибкость при замене технологий


2. 📐 **DRY & KISS** - минимальное дублирование кода и простая структура

    DRY:
  - Единые репозитории с базовыми CRUD операциями в `BaseRepository`
  - Общие мапперы данных в `DataMapper`
  - Утилиты валидации для повторяющихся проверок
  - Стандартизированные обработчики исключений
  
  KISS:
  - Понятная и линейная структура проекта
  - Минимальное количество абстракций там, где они не нужны
  - Четкое разделение ответственности между компонентами
  - Простые и понятные именования


3. ⚡  **SOLID** - Проект следует принципам SOLID:
  - **Single Responsibility** - каждый класс имеет одну ответственность:
    - `HotelService` - управление отелями
    - `RoomValidator` - валидация номеров
    - `AuthService` - аутентификация

  - **Open/Closed** - компоненты открыты для расширения, но закрыты для модификации:
    - Базовые репозитории можно расширять через наследование
    - Валидаторы легко дополнять новыми проверками

  - **Liskov Substitution** - наследники могут заменять родителей:
    - Все репозитории корректно работают через `BaseRepository`
    - Сервисы наследуют общую логику из `BaseService`

  - **Interface Segregation** - клиенты не зависят от неиспользуемых методов:
    - Специализированные DTO для разных сценариев
    - Раздельные схемы для запросов и ответов

  - **Dependency Inversion** - зависимости от абстракций, а не реализаций:
    - Сервисы зависят от абстракций репозиториев
    - Внедрение зависимостей через FastAPI Depends


### Паттерны проектирования
- **DTO** - объект для передачи данных
- **DAO (Repository)** - абстракция доступа к данным
- **Service Layer** - инкапсуляция бизнес-логики
- **Data Mapper** - преобразование между ORM и DTO
- **Dependency Injection** - внедрение зависимостей
- **Strategy** - валидаторы как стратегии проверки

## 📊 Логирование

Комплексное логирование с уровнями INFO, DEBUG, ERROR для:
- Мониторинга работы приложения
- Отладки процессов
- Отслеживания ошибок

## 🔴 Redis

Используется для двух целей:
1. **Кэширование** - ускорение ответов API через FastAPI-Cache
2. **Брокер сообщений** - очередь задач для Celery

## 🔄 Celery и Celery Beat

**Worker** - фоновые задачи:
- Обработка изображений (автоматическое создание ресайзов 1000px, 500px, 200px)
- Тестовые задачи

**Beat** - периодические задачи:
- Ежедневная проверка бронирований с заездом на сегодня
- Уведомления о заезде


## 🛠️ Сборка и запуск проекта
Выполните последовательно команды в терминале:

    git clone https://github.com/stankv/Hotel_Booking_Service.git
    cd Hotel_Booking_Service

Создайте файл **.env** со следующим содержимым:

    MODE=LOCAL
    
    MIN_LENGTH_PASSWORD=3
    
    DB_HOST=booking_db
    DB_PORT=5432
    DB_USER=abcde
    DB_PASS=abcde
    DB_NAME=booking
    
    REDIS_HOST=booking_cache
    REDIS_PORT=6379
    
    JWT_SECRET_KEY=ваш ключ
    JWT_ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

При необходимости измените значения минимальной длины пароля пользователя, имя и пароль базы данных, время жизни JWT-токена.

Сгенерируйте значение JWT_SECRET_KEY выполнив команду в терминале:

    openssl rand -hex 32

Запуск проекта может быть выполнен локально, или в Docker:

Запуск проекта локально
Запуск проекта в Docker

