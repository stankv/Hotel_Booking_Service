<div id="header" align="center">
<img src="https://img.shields.io/badge/Python-black?style=for-the-badge&logo=python&logoColor=yellow"/>&nbsp;
<img src="https://img.shields.io/badge/FastAPI-black?style=for-the-badge&logo=fastapi&logoColor=009688"/>&nbsp;
<img src="https://img.shields.io/badge/SQLAlchemy-black?style=for-the-badge&logo=sqlalchemy&logoColor=D71F00"/>&nbsp;
<img src="https://img.shields.io/badge/Alembic-black?style=for-the-badge&logo=alembic&logoColor=009485"/>&nbsp;
<img src="https://img.shields.io/badge/PostgreSQL-black?style=for-the-badge&logo=PostgreSQL&logoColor=4169E1"/>&nbsp;
<img src="https://img.shields.io/badge/Redis-black?style=for-the-badge&logo=Redis&logoColor=FF4438"/>&nbsp;
<img src="https://img.shields.io/badge/Celery-black?style=for-the-badge&logo=Celery&logoColor=37814A"/>&nbsp;
<img src="https://img.shields.io/badge/PyTest-black?style=for-the-badge&logo=PyTest&logoColor=0A9EDC"/>&nbsp;
<img src="https://img.shields.io/badge/Ruff-black?style=for-the-badge&logo=ruff&logoColor=1B8CF3"/>&nbsp;
<img src="https://img.shields.io/badge/PyRight-black?style=for-the-badge&logo=pyright&logoColor=5EAD66"/>&nbsp;
<img src="https://img.shields.io/badge/Docker-black?style=for-the-badge&logo=docker&logoColor=#07F"/>&nbsp;
<img src="https://img.shields.io/badge/Nginx-black?style=for-the-badge&logo=nginx&logoColor=#00b341"/>&nbsp;
<img src="https://img.shields.io/badge/GitLab_CI-black?style=for-the-badge&logo=gitlab&logoColor=FC6D26"/>&nbsp;
</div>


# Сервис бронирования отелей

Современный REST API для системы бронирования отелей на фреймворке FastAPI с полным стеком технологий.

<img width="975" height="846" alt="изображение" src="https://github.com/user-attachments/assets/813dbe78-0758-4f46-8f45-392177241039" />

## 🎯 Особенности проекта

### 🔐 Аутентификация
- Регистрация/вход (OAuth2 с JWT-токенами)
- Хеширование паролей

### 🏨 Управление данными
- CRUD для отелей, номеров, удобств и бронирований
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
- Валидация всех входных данных
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

### 📁 Структура проекта

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


### Принципы проектирования
1. 🧹 **Чистая Архитектура** - используется многослойная архитектура (Layered Architecture), разделяющая код на независимые слои Domain, Application, Infrastructure, Presentation:

  - **Domain Layer** (`models/`) - Сущности предметной области и бизнес-правила
  - **Application Layer** (`services/`, `schemas/`) - Use Cases и бизнес-логика
  - **Infrastructure Layer** (`repositories/`, `connectors/`) - Внешние системы и БД
  - **Presentation Layer** (`api/`) - API endpoints<br>

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
  - Минимальное количество абстракций, и их отсутствие там где они не нужны
  - Четкое разделение ответственности между компонентами
  - Простые и понятные именования


3. ⚡  **SOLID** - Проект следует принципам SOLID:
  - **Single Responsibility** - например, каждый класс имеет одну ответственность:
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
- **Unit of Work** - управление транзакциями


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


## 🧪 Тестирование и качество кода

Для проекта, развернутого локально:

    pytest -s -v           # Запуск тестов
    ruff check             # Проверка линтинга
    ruff format --check    # Проверка форматирования
    pyright                # Проверка типов

Для проекта, развернутого в Docker:

    docker exec booking_back pytest -s -v           # Запуск тестов
    docker exec booking_back ruff check             # Проверка линтинга
    docker exec booking_back ruff format --check    # Проверка форматирования
    docker exec booking_back pyright                # Проверка типов



## 🛠️ Сборка и запуск проекта
Выполните команды в терминале:

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

При необходимости измените значения минимальной длины пароля пользователя, имя пользователя и пароль к базе данных, время жизни JWT-токена.

Сгенерируйте значение JWT_SECRET_KEY выполнив команду в терминале:

    openssl rand -hex 32

Запуск проекта может быть выполнен локально, или в Docker:

[Запуск проекта локально](https://github.com/stankv/Hotel_Booking_Service/blob/main/docs/start_local.md)

[Запуск проекта в Docker](https://github.com/stankv/Hotel_Booking_Service/blob/main/docs/start_in_docker.md)

