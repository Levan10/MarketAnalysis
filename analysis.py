import yfinance as yf
import pandas as pd
import ta

def fetch_stock_data(ticker: str, period="60mo", interval="1d"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df.dropna(inplace=True)
    return df

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df['sma_20'] = ta.trend.sma_indicator(df['Close'], window=20)
    df['sma_50'] = ta.trend.sma_indicator(df['Close'], window=50)
    df['rsi'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    return df
