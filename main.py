import asyncio
import uvicorn
import threading

from telegram.ext import ApplicationBuilder, ContextTypes
from scanner import generate_premium_signal
from bot import send_premium_signal
from config import TELEGRAM_TOKEN, SYMBOLS, SCAN_INTERVAL

from fastapi_server import app as fastapi_app


async def job(context: ContextTypes.DEFAULT_TYPE):
    for symbol in SYMBOLS:
        signal = generate_premium_signal(symbol)
        if signal:
            await send_premium_signal(context.bot, signal)
            await asyncio.sleep(3)


async def telegram_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.job_queue.run_repeating(job, interval=SCAN_INTERVAL * 60, first=10)

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()


def run_fastapi():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=10000)


if __name__ == "__main__":
    threading.Thread(target=run_fastapi).start()
    asyncio.run(telegram_bot())
