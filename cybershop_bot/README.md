# CYBERSHOP Telegram Bot

Telegram bot for the CYBERSHOP service built with **aiogram 3**.

The bot shows a main menu with inline buttons and collects data from users for
service requests, trade-in, and warranty extension. All answers are stored in
an SQLite database and logged to individual files in `logs/{user_id}`.

## Project structure

```
cybershop_bot/
├── main.py
├── config.py
├── .env.example
├── handlers/
├── keyboards/
├── utils/
├── db/
└── logs/
```

## Database

The bot stores data in an SQLite database using SQLAlchemy's asynchronous
engine. Tables are created on start with `init_db()`.
