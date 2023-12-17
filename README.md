## Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

Технологический стек:
1. Python
2. Flask
3. SQLAlchemy

## Как заполнить .env файл

```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=YOUR_SECRET_KEY 
```

## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:OlegPrizov/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
## Как настроить базу данных с сохранением миграций

Из корневой директории проекта введите команду
```
flask db upgrade
```

## Как запустить проект

Из корневой директории проекта введите команду
```
flask run
```

## Об авторе:

[Олег Призов](https://github.com/OlegPrizov)
