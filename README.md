# Запуск проекта

## Общие требования

- Docker
- Docker Compose

Перед запуском убедитесь, что у вас установлены Docker и Docker Compose.

## Подготовка к запуску

1. Склонируйте репозиторий проекта.
2. Перейдите в каталог проекта.
3. Создайте файл `.env` на основе файла `.env.example` и заполните необходимые значения.

```bash
cp .env.example .env
```

## Запуск на различных операционных системах

### Windows

Откройте командную строку или PowerShell и выполните следующие команды:

```bash
cd путь_к_проекту
```

```bash
docker-compose -f docker-compose.yml up --build --force-recreate
```

### Linux или MacOS

Откройте терминал и выполните следующие команды:

```bash
cd путь_к_проекту
```

```bash
make dev
```

## Задачи

### Задачи софт

- [x] Оптимизировать количество входов в аккаунт
- [x] Оптемизировать маниторинг
- [x] Проблема поднятия
- [x] Таблицы в графическом интерфейсе сделать уже а так же отображение при обновление второй таблицы
- [x] Создать докер образ nginx

- [X] Запрос на закрепление и открепление
- [ ] Создать выбор времени активности
- [X] Опускать если цену нехватает
- [X] Сделать историю вкладку
- [X] Удержание выбраной позиции
- [X] Цена за первое место

### Серверные задачи

- [ ] Оследить момент реакции
- [ ] Требования к серверу
- [ ] Выбрать провайдара

## Примечание

- Сейчас для одного пользователя доступно только одно объявление для поднятия
- Иногда возникает проблема с авторизацией так как при частом входе подает запрос на потверждение через sms (придеться хотя бы один раз зайти в farpost)
- Документация к сервису api находется по ссылки:

1. [docs](http://127.0.0.1:5000/api/v1/docs)
2. [redoc](http://127.0.0.1:5000/api/v1/redoc)
