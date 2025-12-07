import asyncio
from telegram.ext import ApplicationBuilder, ContextTypes
from scanner import generate_premium_signal
from bot import send_premium_signal
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, SYMBOLS, SCAN_INTERVAL
import logging

logging.basicConfig(level=logging.INFO)

async def job(context: ContextTypes.DEFAULT_TYPE):
    for symbol in SYMBOLS:
        signal = generate_premium_signal(symbol)
        if signal:
            await send_premium_signal(context.bot, signal)
            await asyncio.sleep(3)  # чтоб не спамить

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.job_queue.run_repeating(job, interval=SCAN_INTERVAL*60, first=15)
    
    print("Эксклюзивный бот запущен — сигналы только огонь")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
