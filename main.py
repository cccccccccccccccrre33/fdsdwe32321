from dotenv import load_dotenv
load_dotenv()
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Берём токен из переменной окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен и работает!")

# Основная функция
async def main():
    # Создаём приложение
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Регистрируем команду /start
    app.add_handler(CommandHandler("start", start))

    # Запускаем бота
    await app.run_polling()

# Запуск
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
