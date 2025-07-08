from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# ЗАМЕНИ на свой токен
TOKEN = "7718184681:AAGVXEc_xBNiBlAB87OSoQ9EYC0ZIn-XEFU"

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
