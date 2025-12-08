import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Берем токен из Environment Variable
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден. Добавьте Environment Variable на Render")

# Пример простой команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот успешно запущен!")

# Асинхронная функция main для запуска бота
async def main():
    # Создаем приложение бота
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Добавляем обработчик команды /start
    app.add_handler(CommandHandler("start", start))

    # Запускаем бота
    await app.run_polling()

# Стартуем asyncio
if __name__ == "__main__":
    asyncio.run(main())
