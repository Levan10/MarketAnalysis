#To Run , paste " streamlit run app.py " into terminal

from analysis import fetch_stock_data, add_indicators
from strategy import generate_signal
from news import fetch_news


def run_app(ticker):
    print(f"Analyzing {ticker}...")

    df = fetch_stock_data(ticker)
    df = add_indicators(df)
    signal = generate_signal(df)

    print(f"Decision: {signal}\n")

    print("Latest News:")
    for title, url in fetch_news(ticker):
        print(f"- {title}\n  {url}")


if __name__ == "__main__":
    symbol = input("Enter stock ticker (e.g., AAPL): ").upper()
    run_app(symbol)

"""
Stock Analysis Explanation:

This app analyzes a stock using technical indicators — specifically the Simple Moving Averages (SMA) and the Relative Strength Index (RSI) — to generate a basic buy/sell signal. Here's how each part contributes:

SMA (Simple Moving Averages):
   - `SMA20`: Average closing price over the last 20 days (short-term trend)
   - `SMA50`: Average closing price over the last 50 days (medium-term trend)
   - If SMA20 is above SMA50, it indicates upward momentum → Buy signal
   - If SMA20 is below SMA50, it indicates downward momentum → Sell signal

RSI (Relative Strength Index):
   - Measures recent price changes to determine if the stock is overbought or oversold.
   - RSI < 30 = Oversold → Strong Buy (stock may bounce upward)
   - RSI > 70 = Overbought → Strong Sell (stock may drop soon)

Combined Strategy Logic:
   - If SMA20 > SMA50 and RSI < 70 → "Buy"
   - If SMA20 < SMA50 and RSI > 30 → "Sell"
   - If RSI > 70 → "Strong Sell"
   - If RSI < 30 → "Strong Buy"
   - Otherwise → "Hold"

This is a rule-based system and doesn't use machine learning it's meant to give a general directional signal based on momentum and price behavior.
"""
