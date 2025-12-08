import asyncio
import logging
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from scanner import generate_premium_signal
from bot import send_premium_signal, start_command
from config import TELEGRAM_TOKEN, SYMBOLS, SCAN_INTERVAL

logging.basicConfig(level=logging.INFO)

# Функция проверки монет и отправки сигналов
async def job(context: ContextTypes.DEFAULT_TYPE):
    for symbol in SYMBOLS:
        signal = generate_premium_signal(symbol)
        if signal:
            await send_premium_signal(context.bot, signal)
        # Логируем проверку
        logging.info(f"Проверена монета {symbol}, сигнал: {signal}")


async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Команда /start
    app.add_handler(CommandHandler("start", start_command))

    # Добавляем job_queue для периодических проверок
    app.job_queue.run_repeating(job, interval=SCAN_INTERVAL*60, first=15)

    print("Бот запущен — сигналы только огонь 🔥")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
