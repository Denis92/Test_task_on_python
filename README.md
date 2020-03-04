### Инструкция по разворачиванию решения.
1. Клонируем репозиторий
2. git clone -b develop_KODE https://github.com/Denis92/Test_task_on_python.git
3. Переходим в папку с приложением
 
Само решение можно развернуть двумя способами
1. С помощью докера
    1.1
        ```
        docker-compose build
        ```
    после чего должен запуститься web сервер с приложением, а так же база данных mongodb
2. Обычная установка
    2.1 Создаём виртуальное окружение для python командой из консоли (но прежде убедитесь, что вы находитесь в папке с приложением)
        ```
        python -m venv venv
        ```
    2.2 Устанавливаем базу данных mongodb
    2.3 Запускаем приложение командой
        ```
        python app.py
        ```
    сервер будет доступен по адресу http://0.0.0.0:5000
  
### Инструкция по API
Согласно заданию реализовано два метода
1. /send, данный метод позволяет отправить сообщение с пользовательского email адреса, на любой другой, при этом почта с которой отправляется письмо должна быть @yandex.ru

Пример:
Запрос
```
{"login_email":"Denis@yandex.ru", "password_email":"my_password", "message_recipient":"denis@gmail.com", "subject":"Hello", "text":"Hello Denis!"}
```

Ответ
```
{"id": 1583302178.461387, "status": "successful send"}
```
2. /get-result?id_send_email=id, данный метод позволяет получить статус отправки письма по его id

Пример:
Запрос
/get-result?id_send_email=1583302178.461387

Ответ
```
{"id": "1583302178.461387", "datetime": "2020-03-04 06:10:54.756000", "status": "successful send"}
```
