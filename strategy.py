def generate_signal(df):
    latest = df.iloc[-1]

    if latest["sma_20"] > latest["sma_50"] and latest["rsi"] < 70:
        return "Buy"
    elif latest["sma_20"] < latest["sma_50"] and latest["rsi"] > 30:
        return "Sell"
    elif latest["rsi"] > 70:
        return "Strong Sell"
    elif latest["rsi"] < 30:
        return "Strong Buy"
    else:
        return "Hold"
