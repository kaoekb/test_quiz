# Telegram Quiz Bot

Простой Telegram-бот на `aiogram 3`, который проводит мини-тест, считает баллы и показывает итоговый результат.

## Что умеет

- запускает тест по кнопке `Начать тест`
- задает вопросы по очереди через inline-кнопки
- считает итоговый счет
- показывает результат по диапазону баллов
- поддерживает перезапуск через команду `/restart`

## Стек

- Python 3
- aiogram 3
- pydantic-settings
- Docker / Docker Compose

## Подготовка

1. Склонируйте репозиторий и перейдите в папку проекта.
2. Создайте `.env` из примера:

```bash
cp .env.example .env
```

3. Укажите токен бота в `.env`:

```env
BOT_TOKEN=ваш_токен_из_BotFather
```

## Запуск локально

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

## Запуск через Docker

```bash
docker compose up --build -d
```

Логи:

```bash
docker compose logs -f
```

Остановка:

```bash
docker compose down
```

## Команды бота

- `/start` - начать тест
- `/restart` - перезапустить тест

## Структура проекта

```text
.
├── app/
│   ├── main.py        # хендлеры и запуск бота
│   ├── quiz_data.py   # вопросы, ответы, результаты
│   └── config.py      # загрузка BOT_TOKEN из .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```
