import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Загружаем токен из .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен!")

async def main():
    # Создаём приложение бота
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Добавляем обработчик команды /start
    app.add_handler(CommandHandler("start", start))

    # Запускаем бота (новый способ)
    await app.initialize()
    await app.start()
    await app.updater.start_polling()  # можно оставить, но лучше ниже
    await app.run_polling()  # <-- вот здесь реально работает на Render

if __name__ == "__main__":
    asyncio.run(main())
