import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Получаем токен из переменной окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен и готов работать!")

async def main():
    # Создаём приложение
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Регистрируем команду /start
    app.add_handler(CommandHandler("start", start))

    # Запускаем бота
    print("Бот стартовал...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
