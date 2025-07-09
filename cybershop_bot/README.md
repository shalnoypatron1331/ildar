# CYBERSHOP Telegram Bot

Skeleton project for a Telegram bot based on **aiogram 3**.

This repository contains a minimal implementation for collecting user requests
and feedback. Submitted forms are stored in a SQLite database and notifications
are delivered to managers and admins.

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

## Configuration

Create a `.env` file based on `.env.example` and provide your bot token. In
addition to `ADMIN_IDS`, specify `MANAGER_CHAT_ID` with the chat ID of the
manager group where notifications should be sent.

## Notifications

When a user submits a form, the bot sends the formatted information to the
manager chat and to each admin specified in `ADMIN_IDS`. Attachments are stored
inside `media/` and reused for these notifications.

## Installation

Install the required packages using:

```bash
pip install -r requirements.txt
```

## Running the bot

1. Copy `.env.example` to `.env` and fill in the variables:
   - `TOKEN` — Telegram bot token
   - `ADMIN_IDS` — comma separated list of admin Telegram IDs
   - `MANAGER_CHAT_ID` — ID of the manager group chat

2. Launch the bot using:

```bash
python -m cybershop_bot.main
```
