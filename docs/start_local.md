# Запуск проекта локально

1. В последней строке файла **src/main.py**  изменить адрес хоста:


        if __name__ == "__main__":
            uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

2. Установить необходимые пакеты и зависимости - выполнить в корне проекта: 


        pip install -r requirements.txt

3. Установить БД **PostgreSQL**:

   Windows: https://selectel.ru/blog/tutorials/ustanovka-postgresql-15-windows/

   Ubuntu: https://firstvds.ru/technology/ustanovka-postgresql-na-ubuntu

   MacOS: https://ploshadka.net/ustanovka-i-podkljuchenie-postgresql-na-mac-os/  

   или:


        brew install postgresql
        createuser -s postgres
        brew services restart postgresql

4. Для работы с БД установить **DBeaver**:

   Windows: https://practicum.yandex.ru/blog/menedzher-baz-dannyh-dbeaver/

   Ubuntu: https://losst.pro/ustanovka-dbeaver-v-ubuntu-22-04

   MacOS: https://dbeaver.io/download/ (скачайте и запустите)

5. С помощью **DBeaver** создать БД с названием **booking**

6. Выполнить команду для применения миграций:


        alembic upgrade head

7. Установить **Redis**:

   Windows:

   - Способ 1 (через Chocolatey):  https://skillbox.ru/media/base/kak_ustanovit_redis_v_os_windows_bez_ispolzovaniya_docker/

   - Способ 2 (через архивный репозиторий Redis): https://timeweb.cloud/tutorials/redis/ustanovka-i-nastrojka-redis-dlya-raznyh-os

   - Способ 3 (через WSL): https://habr.com/ru/articles/821363/

   Linux: https://help.reg.ru/support/servery-vps/oblachnyye-servery/ustanovka-programmnogo-obespecheniya/kak-ustanovit-i-nastroit-redis-na-linux#2

   MacOS: 


        brew install redis****

8. Установить **Celery**:


        pip install celery

9. Для запуска приложения выполнить в терминале:


        python src/main.py

10. Для запуска **Celery** (worker и beat) в Linux выполнить команду в другом терминале:


        celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

11. Для запуска **Celery** в Windows:


        # Если нужен только worker, то выполнить в другом терминале:
        celery -A src.tasks.celery_app:celery_instance worker -l INFO --pool=solo
        
        # Если нужны и worker и beat:
        celery -A src.tasks.celery_app:celery_instance worker -l INFO --pool=solo    # запуск worker (во 2-м терминале)
        celery -A src.tasks.celery_app:celery_instance beat -l INFO                  # запуск beat (в 3-м терминале)