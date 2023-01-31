# Домашнее задание #3 от YLAB "Вынести бизнес логику и запросы в БД в отдельные слои приложения. Добавить кеширование Redis. Добавить pre-commit хуки. Описать ручки API в соответствии с OpenAPI.".

**Установка:**
```
git clone https://github.com/Arty3m/ylab_2023-hw3.git
```

**Для запуска через docker compose необходимо использовать команду:**

```
docker-compose up -d --build
```

**Запуск тестов:**

```
docker-compose -f docker-compose.tests.yml up -d --build
```

**Документация доступна по адресу:**
```
http://localhost:8000/api/openapi
ИЛИ
http://localhost:8000/api/redoc
```

**Запустить Postman тесты**
