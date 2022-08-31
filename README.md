![finaltask](https://github.com/airatbakiev/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Foodgram - социальная сеть о кулинарных рецептах.

### Стек

- Python 3.7.0
- Django 2.2.16
- DRF 3.12.4
- Nginx
- Docker-compose

### Описание

Это итоговая дипломная работа курса "Python-разработчик".

### Результат

Описать

### Ресурсы API YaMDb

- Ресурс ***auth***: аутентификация, получение токена.
- Ресурс ***users***: пользователи, подписки на авторов.
- Ресурс ***recipes***: рецепты, избранные рецепты, список покупок.
- Ресурс ***tags***: теги к рецептам.
- Ресурс ***ingredients***: ингредиенты для рецептов.

Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.
***Путь к документации (redoc) в блоке описания запуска проекта***.

### Как запустить проект:

1. Клонировать репозиторий:

```
git clone https://github.com/airatbakiev/foodgram-project-react.git
```

2. Добавить в клонированный репозиторий секреты (Settings/Secrets):

```
Переменная: USER, значение: <имя пользователя для подключения к серверу>
```
```
Переменная: HOST, значение: <публичный ip-адрес сервера>
```
```
Переменная: SSH, значение: <закрытый ssh-ключ для подключения к серверу>
```
```
Переменная: PASSPHRASE, значение: <пароль, если ssh-ключ защищён паролем>
```
```
Переменная: DOCKER_USERNAME, значение: <имя пользователя для поключения к DockerHub>
```
```
Переменная: DOCKER_PASSWORD, значение: <пароль для поключения к DockerHub>
```
```
Переменная: DB_ENGINE, значение: django.db.backends.postgresql
```
```
Переменная: DB_HOST, значение: db
```
```
Переменная: DB_NAME, значение: postgres
```
```
Переменная: DB_PORT, значение: 5432
```
```
Переменная: POSTGRES_USER, значение: postgres
```
```
Переменная: POSTGRES_PASSWORD, значение: postgres
```

3. На сервере установить пакеты docker.io и docker-compose v2.6.1

4. Перейти в папку
```
foodgram-project-react/infra
```

5. Запустить сборку контейнеров
```
sudo docker-compose up -d
```

6. В контейнере web выполнить миграции
```
sudo docker-compose exec web python manage.py makemigrations
```
```
sudo docker-compose exec web python manage.py migrate
```

7. В контейнере web собрать статику и создать суперпользователя

```
sudo docker-compose exec web python manage.py collectstatic
```
```
sudo docker-compose exec web python manage.py createsuperuser
```

### Проверьте работоспособность приложения, для этого перейдите на страницы:

[http://<ip-адрес сервера>/admin/](http://51.250.101.69/admin/)

[http://<ip-адрес сервера>/api/recipes/](http://51.250.101.69/)

***Документация*** (запросы для работы с API):

[http://<ip-адрес сервера>/api/redoc](http://51.250.101.69/api/docs/)


### Автор проекта:

```
Айрат Бакиев
```

### Лицензия

[MIT](./LICENSE)