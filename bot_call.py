from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env located next to this script
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

# The bot token is read from the environment
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN not provided in .env")

# Команда /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я твой бот. Напиши что-нибудь!")

# Ответ на любые текстовые сообщения
def echo(update: Update, context: CallbackContext):
    user_text = update.message.text
    update.message.reply_text(f"Ты написал: {user_text}")

# Основной блок запуска
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Обработчики команд и сообщений
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запуск бота
    updater.start_polling()
    print("Бот запущен...")
    updater.idle()

if __name__ == "__main__":
    main()
