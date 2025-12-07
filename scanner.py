import ccxt
import pandas as pd
import numpy as np
from config import SYMBOLS, TIMEFRAME

exchange = ccxt.bybit({'enableRateLimit': True, 'options': {'defaultType': 'swap'}})

def get_df(symbol, tf=TIMEFRAME, limit=200):
    try:
        bars = exchange.fetch_ohlcv(symbol, tf, limit=limit)
        df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'volume'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        return df
    except:
        return None

def is_bullish_structure(df):
    recent = df.iloc[-10:]
    return recent['high'].max() == recent['high'].iloc[-1] or recent['high'].iloc[-1] > recent['high'].iloc[-3]

def is_bearish_structure(df):
    recent = df.iloc[-10:]
    return recent['low'].min() == recent['low'].iloc[-1] or recent['low'].iloc[-1] < recent['low'].iloc[-3]

def volume_delta_spike(df):
    avg_vol = df['volume'].rolling(20).mean().iloc[-1]
    return df['volume'].iloc[-1] > avg_vol * 2.5

def get_4h_trend(symbol):
    df = get_df(symbol, "4h", 50)
    if df is None: return None
    ema50 = df['close'].ewm(span=50).mean().iloc[-1]
    ema200 = df['close'].ewm(span=200).mean().iloc[-1]
    price = df['close'].iloc[-1]
    if price > ema50 > ema200: return "BULL"
    if price < ema50 < ema200: return "BEAR"
    return "SIDE"

def generate_premium_signal(symbol):
    df = get_df(symbol)
    if df is None or len(df) < 100: return None

    price = df['close'].iloc[-1]
    atr = (df['high'] - df['low']).rolling(14).mean().iloc[-1]
    trend_4h = get_4h_trend(symbol)

    # ЛОНГ — только в бычьем тренде 4h + структура + объём
    if (trend_4h == "BULL" and 
        is_bullish_structure(df) and 
        volume_delta_spike(df) and
        df['close'].iloc[-1] > df['open'].iloc[-1]):  # зелёная свеча

        leverage = 20 if atr > price * 0.01 else 12
        return {
            "symbol": symbol.replace(":USDT", ""),
            "side": "LONG",
            "entry": round(price, 6),
            "sl": round(price - atr * 1.8, 6),
            "tp1": round(price + atr * 2.5, 6),
            "tp2": round(price + atr * 5, 6),
            "tp3": "Trailing +2%",
            "leverage": leverage,
            "strength": "HIGH" if leverage >= 20 else "MEDIUM"
        }

    # ШОРТ
    if (trend_4h == "BEAR" and 
        is_bearish_structure(df) and 
        volume_delta_spike(df) and
        df['close'].iloc[-1] < df['open'].iloc[-1]):

        leverage = 20 if atr > price * 0.01 else 12
        return {
            "symbol": symbol.replace(":USDT", ""),
            "side": "SHORT",
            "entry": round(price, 6),
            "sl": round(price + atr * 1.8, 6),
            "tp1": round(price - atr * 2.5, 6),
            "tp2": round(price - atr * 5, 6),
            "tp3": "Trailing +2%",
            "leverage": leverage,
            "strength": "HIGH" if leverage >= 20 else "MEDIUM"
        }

    return None
