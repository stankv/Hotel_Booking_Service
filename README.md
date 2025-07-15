<div id="header" align="center">
<img src="https://img.shields.io/badge/Python-black?style=for-the-badge&logo=python&logoColor=yellow"/>&nbsp;
<img src="https://img.shields.io/badge/FastAPI-black?style=for-the-badge&logo=fastapi&logoColor=009688"/>&nbsp;
<img src="https://img.shields.io/badge/SQLAlchemy-black?style=for-the-badge&logo=sqlalchemy&logoColor=D71F00"/>&nbsp;
<img src="https://img.shields.io/badge/PostgreSQL-black?style=for-the-badge&logo=PostgreSQL&logoColor=4169E1"/>&nbsp;
<img src="https://img.shields.io/badge/Redis-black?style=for-the-badge&logo=Redis&logoColor=FF4438"/>
<img src="https://img.shields.io/badge/Celery-black?style=for-the-badge&logo=Celery&logoColor=37814A"/>
<img src="https://img.shields.io/badge/PyTest-black?style=for-the-badge&logo=PyTest&logoColor=0A9EDC"/>
<img src="https://img.shields.io/badge/HTML-black?style=for-the-badge&logo=HTML5&logoColor=E34F26"/>&nbsp;
<img src="https://img.shields.io/badge/CSS-black?style=for-the-badge&logo=CSS3&logoColor=1572B6"/>&nbsp;
</div>


# Сервис бронирования отелей
В разработке...

## Запуск сервисов в Docker по отдельности:

Перед запуском контейнеров пропишите в файле конфигурации ***.env*** (в корне каталога) 
имя пользователя и пароль для подключения к БД, и затем эти же данные в параметрах 
команды запуска контейнера с БД (п.5).

1. Сборка образа с приложением: 

        sudo docker build -t booking_image .

2. Создание docker-сети: 

        sudo docker network create myNetwork

3. Создание и запуск контейнера с nginx:
    
        sudo docker run --name booking_nginx \
            -v ./nginx.conf:/etc/nginx/nginx.conf \
            --network=myNetwork \
            --rm -p 80:80 nginx

4. Создание и запуск контейнера с приложением:

        sudo docker run --name booking_back \
            -p 7777:8000 \
            --network=myNetwork \
            booking_image

5. Создание и запуск контейнера с БД PostgreSQL:

        sudo docker run --name booking_db \
            -p 6432:5432 \
            -e POSTGRES_USER=ваше_имя_пользователя \
            -e POSTGRES_PASSWORD=ваш_пароль \
            -e POSTGRES_DB=booking \
            --network=myNetwork \
            --volume pg-booking-data:/var/lib/postgresql/data \
            -d postgres:16

6. Создание и запуск контейнера с Redis:

        sudo docker run --name booking_cache \
            -p 7379:6379 \
            --network=myNetwork \
            -d redis:7.4

7. Создание и запуск контейнера с Celery:

        sudo docker run --name booking_celery_worker \
            --network=myNetwork \
            booking_image \
            celery --app=src.tasks.celery_app:celery_instance worker -l INFO

8. Создание и запуск контейнера с Celery beat:

        sudo docker run --name booking_celery_beat \
            --network=myNetwork \
            booking_image \
            celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

