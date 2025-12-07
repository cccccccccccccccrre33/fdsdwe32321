from config import TELEGRAM_CHAT_ID

async def send_premium_signal(bot, signal):
    emoji = "🔥" if signal["strength"] == "HIGH" else "🚀"
    text = f"""
{emoji} ПРЕМИУМ СИГНАЛ {emoji}

{signal['symbol']} | {signal['side']}
Сила: {signal['strength']}

Вход: {signal['entry']}
Плечо: ×{signal['leverage']}

SL: {signal['sl']}
TP1 (1:2.5): {signal['tp1']}
TP2 (1:5): {signal['tp2']}
TP3: {signal['tp3']}

Только для своих 
    """.strip()

    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
