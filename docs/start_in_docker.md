# Запуск проекта в Docker

## Запуск сервисов проекта в контейнерах по отдельности

1. Установить Docker:

   Windows: https://sendel.ru/shorts/install-docker-windows/

   Linux: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository  (запустите все команды, которые перечислены в этом разделе)

   MacOS: https://www.heyvaldemar.net/ustanovka-docker-desktop-na-macos/

2. Создать docker-сеть с названием myNetwork:

       docker network create myNetwork
3. Создать и запустить контейнер с **PostgreSQL** с названием booking_db:

        docker run --name booking_db \
            -p 6432:5432 \
            -e POSTGRES_USER=abcde \
            -e POSTGRES_PASSWORD=abcde \
            -e POSTGRES_DB=booking \
            --network=myNetwork \
            --volume pg-booking-data:/var/lib/postgresql/data \
            -d postgres:16

4. Создать и запустить контейнер с **Redis** с названием booking_cache:

        docker run --name booking_cache \
            -p 7379:6379 \
            --network=myNetwork \
            -d redis:7.4

5. Создать и запустить контейнер с **Celery Worker** с названием booking_celery_worker:

        docker run --name booking_celery_worker \
            --network=myNetwork \
            booking_image \
            celery --app=src.tasks.celery_app:celery_instance worker -l INFO

6. Создать и запустить контейнер с **Celery beat** с названием booking_celery_beat:

        docker run --name booking_celery_beat \
            --network=myNetwork \
            booking_image \
            celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

7. Раскомментировать порты в файле docker-compose.yml

8. Находясь в корне проекта выполнить сборку образа с приложением:

        docker build -t booking_image .

9. Создать и запустить контейнер с приложением:

        docker run --name booking_back \
            -p 7777:8000 \
            --network=myNetwork \
            booking_image

Проект будет доступен по адресу: http://127.0.0.1:7777

## Запуск сервисов проекта с помощью Docker Compose

1. Выполнить пункты 1-4 предыдущего раздела

2. Находясь в корне проекта выполнить команду в терминале:

         docker compose up --build -d

3. Чтобы смотреть логи приложения в реальном времени, выполнить команду:

         docker logs --follow booking_back

Проект будет доступен по адресу: http://127.0.0.1:7777

После запуска всех контейнеров можно (не обязательно) развернуть контейнер с сервером **Nginx**. Для этого:

1. Порты в файле docker-compose.yml должны быть закомментированы

2. В репозитории версия файла настроек nginx.conf с устанолвленными SSL-сертификатами для production. Нужно изменить его содержимое на:

        events {}
        
        http {
            limit_req_zone $binary_remote_addr zone=mylimit:10m rate=5r/s;
        
            server {
                limit_req zone=mylimit;
                location / {
                    proxy_pass http://booking_back:8000/;
                }
            }
        }

3. Выполнить команду в терминале:

        docker run --name booking_nginx \
            -v ./nginx.conf:/etc/nginx/nginx.conf \
            --network=myNetwork \
            --rm -p 80:80 nginx

Проект будет доступен по адресу: http://127.0.0.1
