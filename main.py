import asyncio
import logging
from telegram.ext import ApplicationBuilder, ContextTypes
from scanner import generate_premium_signal
from bot import send_premium_signal
from config import TELEGRAM_TOKEN, SYMBOLS, SCAN_INTERVAL

logging.basicConfig(level=logging.INFO)

async def job(context: ContextTypes.DEFAULT_TYPE):
    for symbol in SYMBOLS:
        try:
            signal = generate_premium_signal(symbol)
            if signal:
                await send_premium_signal(context.bot, signal)
                await asyncio.sleep(2)
        except Exception as e:
            logging.error(f"Ошибка на символе {symbol}: {e}")

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Запуск job каждые N минут
    app.job_queue.run_repeating(job, interval=SCAN_INTERVAL * 60, first=10)

    print("🚀 Бот запущен — жду сигналы...")

    # ВНИМАНИЕ: для версии 20 используется только run_polling
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
