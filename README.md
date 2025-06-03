# cardboard_production_control
Программа учета продукции и сырья для картонажного производства


Для развертывания приложения нужно:
- Установить на компьютер: Git, Python3, Docker и Docker-Compouse.
- Склонировать git репозиторий на компьютер.


    $ git clone https://github.com/DorofeevAlexandr/cardboard_production_control.git

- Собрать образы командой. 


    $ sudo docker compose build

- Запустить контейнеры командой.


    $ sudo docker compose up -d

---
Запустить миграцию:

    $ docker-compose exec web python manage.py migrate --noinput
---
 Создайте суперпользователя командой:

    $ docker-compose exec web python manage.py createsuperuser 
---


    sudo docker compose down
    sudo docker compose build
    sudo docker compose up -d
    sudo docker ps -a
    
    sudo docker-compose logs -f

---
    sudo docker compose down
    sudo docker-compose -f docker-compose.yml down
    sudo docker-compose -f docker-compose.yml up -d --build
---
    sudo docker-compose -f docker-compose.yml up -d --build
    sudo docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
    sudo docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
---



