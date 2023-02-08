# Домашнее задание #4 от YLAB "Переписать FastAPI приложение на асинхронное выполнение. Добавить в проект фоновую задачу с помощью Celery + RabbitMQ.".

**Установка:**
```
git clone https://github.com/Arty3m/ylab_2023-hw4.git
```

**Для запуска через docker compose необходимо использовать команду:**

```
docker-compose up -d --build
```

**Запуск тестов:**

```
docker-compose -f docker-compose.tests.yml up -d --build
```
**Запустить Postman тесты**

+ БД должна быть пустая

**Сформировать меню в виде excel файла**

```
1. Перейти на http://localhost:8000/api/v1/create_full_menu для заполнения БД данными
2. Перейти на http://localhost:8000/api/v1/task для создания задачи на создание excel файла и получить её task_id
3. Перейти на http://localhost:8000/api/v1/task/{task_id} и получить сформированный excel файл по task_id
ИЛИ
Воспользоваться документацией openapi
```

**Документация доступна по адресу:**
```
http://localhost:8000/api/openapi
or
http://localhost:8000/api/redoc
```
