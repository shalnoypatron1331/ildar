# CYBERSHOP Telegram Bot

Skeleton project for a Telegram bot based on **aiogram 3**.

This repository contains the initial structure and database setup. The bot will be
implemented later.

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
